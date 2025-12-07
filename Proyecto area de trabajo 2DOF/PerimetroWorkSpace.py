"""
Interfaz Tkinter para:
- Configurar parámetros del robot 2-DOF
- Calcular workspace (alpha-shape), perímetro, area
- Guardar contorno en JSON y DXF
- Ingresar punto A y B
- Calcular ruta (recta o por nodos seguros) y convertir a ángulos (IK)
- Guardar trayectoria en JSON
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import alphashape
from shapely.geometry import Point, LineString, Polygon
import ezdxf
import json
import math
import heapq
import random
import os

# ------------------------------
# Parámetros por defecto
# ------------------------------
DEFAULTS = {
    "ri1": 60.0, "rf1": 90.0,
    "ri2": -145.0, "rf2": -110.0,
    "l1": 10.0, "l2": 8.0,
    "condicion1": 80.0, "condicion2": 145.0,
    "alpha": 0.3
}

# Parámetros nodos/planificador
NUM_NODOS = 600
K_NEIGHBORS = 8
SAMPLES_SEGMENT = 20

# Globals que se llenan tras calcular workspace
_workspace_points = None     # np.array Nx2
_shape_polygon = None        # shapely polygon
_contour_xy = None           # list of (x,y)
_x_points = None
_y_points = None

# ------------------------------
# Funciones de sistema experto (configurables por UI)
# ------------------------------
def make_rules(ri1, rf1, ri2, rf2, condicion1, usar_cond1, condicion2, usar_cond2):
    # Devuelve funciones regla1..regla5 y es_postura_valida cerradas sobre esos parámetros
    def regla1(theta1_deg):
        return ri1 <= theta1_deg <= rf1
    def regla2(theta2_deg):
        return ri2 <= theta2_deg <= rf2
    def regla3(theta1_deg, theta2_deg):
        if not usar_cond1:
            return True
        return 180.0 + theta2_deg > condicion1 - theta1_deg
    def regla4(theta1_deg, theta2_deg):
        return not (theta1_deg > (rf1 - 5.0) and theta2_deg < (ri2 + 5.0))
    def regla5(theta1_deg, theta2_deg):
        if not usar_cond2:
            return True
        return 180.0 + theta2_deg < condicion2 - theta1_deg
    def es_postura_valida(theta1_deg, theta2_deg):
        return (regla1(theta1_deg) and regla2(theta2_deg) and regla3(theta1_deg, theta2_deg)
                and regla4(theta1_deg, theta2_deg) and regla5(theta1_deg, theta2_deg))
    return regla1, regla2, regla3, regla4, regla5, es_postura_valida

# ------------------------------
# Cinemática directa (simplemente para construir workspace)
# ------------------------------
def forward_kinematics(l1, l2, theta1_rad, theta2_rad):
    x = l1 * math.cos(theta1_rad) + l2 * math.cos(theta1_rad + theta2_rad)
    y = l1 * math.sin(theta1_rad) + l2 * math.sin(theta1_rad + theta2_rad)
    return x, y

# ------------------------------
# Cinemática inversa (2 soluciones max)
# ------------------------------
def inverse_kinematics(x, y, l1, l2):
    d2 = x*x + y*y
    L1 = l1; L2 = l2
    cos_theta2 = (d2 - L1*L1 - L2*L2) / (2.0 * L1 * L2)
    if cos_theta2 < -1.0 or cos_theta2 > 1.0:
        return []
    sin_pos = math.sqrt(max(0.0, 1.0 - cos_theta2*cos_theta2))
    sin_neg = -sin_pos
    theta2_a = math.atan2(sin_pos, cos_theta2)
    theta2_b = math.atan2(sin_neg, cos_theta2)
    def calc_theta1(theta2):
        k1 = L1 + L2 * math.cos(theta2)
        k2 = L2 * math.sin(theta2)
        theta1 = math.atan2(y, x) - math.atan2(k2, k1)
        return theta1
    theta1_a = calc_theta1(theta2_a)
    theta1_b = calc_theta1(theta2_b)
    def to_deg_norm(rad):
        deg = math.degrees(rad)
        deg = ((deg + 180.0) % 360.0) - 180.0
        return deg
    sol = []
    sol.append((to_deg_norm(theta1_a), to_deg_norm(theta2_a)))
    sol.append((to_deg_norm(theta1_b), to_deg_norm(theta2_b)))
    # filtrar duplicados
    unique = []
    for s in sol:
        if not any(math.isclose(s[0], u[0], abs_tol=1e-6) and math.isclose(s[1], u[1], abs_tol=1e-6) for u in unique):
            unique.append(s)
    return unique

# ------------------------------
# Verificación si punto/segmento dentro del polygon
# ------------------------------
def punto_en_area(shape, p):
    return shape.contains(Point(p)) or shape.touches(Point(p))

def segmento_valido(shape, p, q, samples=SAMPLES_SEGMENT):
    for t in np.linspace(0, 1, samples):
        x = p[0] + (q[0] - p[0]) * t
        y = p[1] + (q[1] - p[1]) * t
        if not punto_en_area(shape, (x, y)):
            return False
    return True

# ------------------------------
# Generador de nodos seguros
# ------------------------------
def generar_nodos_seguros(shape, num_nodos=NUM_NODOS, seed=0):
    random.seed(seed); np.random.seed(seed)
    minx, miny, maxx, maxy = shape.bounds
    nodes = []
    intentos = 0
    while len(nodes) < num_nodos and intentos < num_nodos * 30:
        x = np.random.uniform(minx, maxx)
        y = np.random.uniform(miny, maxy)
        if punto_en_area(shape, (x, y)):
            nodes.append((float(x), float(y)))
        intentos += 1
    if len(nodes) < num_nodos:
        print(f"Advertencia: solo se generaron {len(nodes)} nodos (solicitados {num_nodos}).")
    return nodes

# ------------------------------
# Construcción grafo y Dijkstra
# ------------------------------
def euclid(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def construir_grafo(nodes, shape, k=K_NEIGHBORS):
    n = len(nodes)
    adj = {i: [] for i in range(n)}
    coords = np.array(nodes)
    dists = np.sqrt(((coords[:, None, :] - coords[None, :, :])**2).sum(axis=2))
    for i in range(n):
        inds = np.argsort(dists[i])
        cnt = 0
        for j in inds[1:]:
            if cnt >= k:
                break
            p = tuple(coords[i]); q = tuple(coords[j])
            if segmento_valido(shape, p, q):
                dist = float(dists[i, j])
                adj[i].append((int(j), dist))
                cnt += 1
    for i in range(n):
        for j, dist in list(adj[i]):
            if not any(nb == i for nb, _ in adj[j]):
                adj[j].append((i, dist))
    return adj

def dijkstra(adj, start_idx, goal_idx):
    pq = [(0.0, start_idx)]
    dist = {start_idx: 0.0}
    prev = {}
    visited = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == goal_idx:
            break
        for v, w in adj.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if goal_idx not in dist:
        return None
    path = []
    cur = goal_idx
    while cur != start_idx:
        path.append(cur)
        cur = prev[cur]
    path.append(start_idx)
    path.reverse()
    return path

# ------------------------------
# Función para calcular workspace y contorno (alpha-shape)
# ------------------------------
def calcular_workspace_and_contorno(params, plot_axes=None):
    """
    params: dict con keys: ri1, rf1, ri2, rf2, l1, l2, condicion1, usar_cond1, condicion2, usar_cond2, alpha, paso
    plot_axes: matplotlib axes opcional para dibujar (si None no dibuja)
    Retorna: (shape_polygon, points_array, contour_xy, perimeter, area)
    """
    ri1 = float(params["ri1"]); rf1 = float(params["rf1"])
    ri2 = float(params["ri2"]); rf2 = float(params["rf2"])
    l1 = float(params["l1"]); l2 = float(params["l2"])
    condicion1 = float(params["condicion1"]); usar_cond1 = bool(params["usar_cond1"])
    condicion2 = float(params["condicion2"]); usar_cond2 = bool(params["usar_cond2"])
    alpha = float(params.get("alpha", DEFAULTS["alpha"]))
    paso = int(params.get("paso", 1))

    rango1 = np.arange(ri1, rf1 + paso, paso)
    rango2 = np.arange(ri2, rf2 + paso, paso)
    r1_rad = np.deg2rad(rango1)
    r2_rad = np.deg2rad(rango2)

    # reglas cerradas
    _, _, _, _, _, es_postura_valida = make_rules(ri1, rf1, ri2, rf2, condicion1, usar_cond1, condicion2, usar_cond2)

    x_points = []
    y_points = []
    for th1 in r1_rad:
        for th2 in r2_rad:
            th1_deg = np.rad2deg(th1); th2_deg = np.rad2deg(th2)
            if not es_postura_valida(th1_deg, th2_deg):
                continue
            x, y = forward_kinematics(l1, l2, th1, th2)
            x_points.append(float(x)); y_points.append(float(y))
    if len(x_points) < 10:
        raise RuntimeError("Pocos puntos generados para el workspace. Revisa rangos y reglas.")

    points = np.column_stack((x_points, y_points))
    # alpha-shape
    shape = alphashape.alphashape(points, alpha)
    if shape.geom_type == 'MultiPolygon':
        shape = max(shape, key=lambda p: p.area)
    if not isinstance(shape, Polygon):
        raise RuntimeError("AlphaShape no produjo un polígono (ajusta alpha).")

    perimetro = float(shape.length)
    area = float(shape.area)
    x_cont, y_cont = shape.exterior.xy
    contour_xy = list(zip(map(float, x_cont), map(float, y_cont)))
    # dibujar si se pasa axes
    if plot_axes is not None:
        ax = plot_axes
        ax.clear()
        ax.scatter(points[:,0], points[:,1], s=6, alpha=0.3, label="Workspace (muestras)")
        ax.plot([c[0] for c in contour_xy], [c[1] for c in contour_xy], 'r-', linewidth=2, label="Contorno (alpha-shape)")
        ax.set_aspect('equal', 'box')
        ax.grid(True)
        ax.legend()
    return shape, points, contour_xy, perimetro, area

# ------------------------------
# GUI: Tkinter
# ------------------------------
class WorkspaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Workspace 2-DOF - Sistema Experto y Planificación")
        self.geometry("1150x700")

        # Frame izquierdo: controles
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        # Parámetros - entradas
        lbl = ttk.Label(ctrl_frame, text="Parámetros del robot", font=("Segoe UI", 11, "bold"))
        lbl.pack(pady=4)

        self.entries = {}
        def add_row(key, label, default):
            row = ttk.Frame(ctrl_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label, width=18).pack(side=tk.LEFT)
            var = tk.StringVar(value=str(default))
            ent = ttk.Entry(row, textvariable=var, width=12)
            ent.pack(side=tk.LEFT)
            self.entries[key] = var

        add_row("ri1", "Ang. inicio 1 (°)", DEFAULTS["ri1"])
        add_row("rf1", "Ang. final 1 (°)", DEFAULTS["rf1"])
        add_row("ri2", "Ang. inicio2 (°)", DEFAULTS["ri2"])
        add_row("rf2", "Ang. final2 (°)", DEFAULTS["rf2"])
        add_row("l1",  "Largo 1 (unid.)", DEFAULTS["l1"])
        add_row("l2",  "Largo 2 (unid.)", DEFAULTS["l2"])
        add_row("condicion1", "condición1 (°)", DEFAULTS["condicion1"])
        add_row("condicion2", "condición2 (°)", DEFAULTS["condicion2"])
        add_row("alpha", "alpha (0.1-1.0)", DEFAULTS["alpha"])

        # Checkbuttons para activar reglas
        chk_frame = ttk.Frame(ctrl_frame)
        chk_frame.pack(fill=tk.X, pady=6)
        self.var_cond1 = tk.BooleanVar(value=True)
        self.var_cond2 = tk.BooleanVar(value=False)
        ttk.Checkbutton(chk_frame, text="Usar 180 - Ang2 > condición1 -  Ang. 1", variable=self.var_cond1).pack(anchor=tk.W)
        ttk.Checkbutton(chk_frame, text="Usar 180 - Ang2 < condición2 -  Ang. 1", variable=self.var_cond2).pack(anchor=tk.W)

        # Botón seleccionar carpeta de guardado
        btn_select_dir = ttk.Button(ctrl_frame, text="Seleccionar carpeta de guardado", command=self.on_select_folder)
        btn_select_dir.pack(fill=tk.X, pady=6)
        self.save_dir = os.getcwd()

        # Botón calcular workspace
        btn_calc = ttk.Button(ctrl_frame, text="Calcular área y perímetro", command=self.on_calcular_workspace)
        btn_calc.pack(fill=tk.X, pady=8)

        # Etiquetas de resultado
        self.lbl_perimetro = ttk.Label(ctrl_frame, text="Perímetro: -")
        self.lbl_perimetro.pack(anchor=tk.W, pady=2)
        self.lbl_area = ttk.Label(ctrl_frame, text="Área: -")
        self.lbl_area.pack(anchor=tk.W, pady=2)

        # Sección puntos A/B (deshabilitada hasta calcular)
        ttk.Separator(ctrl_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)
        lbl2 = ttk.Label(ctrl_frame, text="Puntos A & B (una vez calculado workspace)", font=("Segoe UI", 10, "bold"))
        lbl2.pack(pady=4)
        self.puntoA_var = tk.StringVar(value="12.0,3.0")
        self.puntoB_var = tk.StringVar(value="5.0,10.0")
        entA = ttk.Entry(ctrl_frame, textvariable=self.puntoA_var, width=18, state=tk.DISABLED)
        entA.pack(pady=2)
        entB = ttk.Entry(ctrl_frame, textvariable=self.puntoB_var, width=18, state=tk.DISABLED)
        entB.pack(pady=2)
        self.entry_puntoA = entA; self.entry_puntoB = entB

        # Botón planificar ruta (deshabilitado hasta calcular workspace)
        self.btn_plan = ttk.Button(ctrl_frame, text="Calcular ruta y cinemática", command=self.on_calcular_trayectoria, state=tk.DISABLED)
        self.btn_plan.pack(fill=tk.X, pady=8)

        # Log simple
        self.log = tk.Text(ctrl_frame, height=12, width=36)
        self.log.pack(pady=6)

        # Frame derecho: Matplotlib
        plot_frame = ttk.Frame(self)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.fig, self.ax = plt.subplots(figsize=(7,7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # estado
        self.workspace_computado = False

    def log_msg(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def on_select_folder(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.save_dir = path
            self.log_msg(f"Carpeta seleccionada: {path}")


    def on_calcular_workspace(self):
        # Leer parámetros de UI
        try:
            params = {}
            for k, var in self.entries.items():
                params[k] = float(var.get())
            params["usar_cond1"] = bool(self.var_cond1.get())
            params["usar_cond2"] = bool(self.var_cond2.get())
            params["alpha"] = float(self.entries["alpha"].get())
            params["paso"] = 1
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")
            return
        self.log_msg("Calculando workspace... esto puede tardar unos segundos.")
        try:
            shape, points, contour_xy, perimetro, area = calcular_workspace_and_contorno(params, plot_axes=self.ax)
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al calcular workspace: {e}")
            self.log_msg(f"Error: {e}")
            return

        # Guardar globales
        global _workspace_points, _shape_polygon, _contour_xy, _x_points, _y_points
        _workspace_points = points
        _shape_polygon = shape
        _contour_xy = contour_xy
        _x_points = points[:,0]; _y_points = points[:,1]

        # Actualizar GUI
        self.lbl_perimetro.config(text=f"Perímetro: {perimetro:.3f}")
        self.lbl_area.config(text=f"Área: {area:.3f}")
        self.canvas.draw()
        self.log_msg(f"Workspace calculado. Perímetro={perimetro:.3f}, Área={area:.3f}")

        # Guardar contorno en JSON y DXF
        try:
            json_path = os.path.join(self.save_dir, "contorno_robot.json")

            with open(json_path, "w") as f:
                json.dump({"contorno": [{"x": float(x), "y": float(y)} for x, y in contour_xy]}, f, indent=4)
            dxf_path = os.path.join(self.save_dir, "contorno_robot.dxf")

            doc = ezdxf.new()
            msp = doc.modelspace()
            msp.add_lwpolyline(contour_xy, close=True)
            doc.saveas(dxf_path)
            self.log_msg(f"Contorno guardado: {json_path}, {dxf_path}")
        except Exception as e:
            self.log_msg(f"Advertencia: no se pudo guardar archivos contorno: {e}")

        # habilitar entrada de puntos y boton de planificacion
        self.entry_puntoA.config(state=tk.NORMAL)
        self.entry_puntoB.config(state=tk.NORMAL)
        self.btn_plan.config(state=tk.NORMAL)
        self.workspace_computado = True

    def parse_point_str(self, s):
        try:
            parts = s.split(",")
            x = float(parts[0].strip()); y = float(parts[1].strip())
            return (x, y)
        except Exception:
            raise ValueError("Formato punto inválido. Use 'x,y' ejemplo: 12.0,3.0")

    def on_calcular_trayectoria(self):
        if not self.workspace_computado:
            messagebox.showwarning("Atención", "Primero calcule el workspace.")
            return
        try:
            pA = self.parse_point_str(self.puntoA_var.get())
            pB = self.parse_point_str(self.puntoB_var.get())
        except Exception as e:
            messagebox.showerror("Error", f"Puntos inválidos: {e}")
            return

        shape = _shape_polygon
        registro = []

        # Verificar A y B dentro area
        A_val = punto_en_area(shape, pA)
        B_val = punto_en_area(shape, pB)
        registro.append(f"A en área: {A_val}; B en área: {B_val}")
        if not (A_val and B_val):
            messagebox.showerror("Error", "Uno o ambos puntos están fuera del área de trabajo.")
            self.log_msg("\n".join(registro))
            return

        # Verificar recta
        if segmento_valido(shape, pA, pB):
            registro.append("La recta A->B está dentro del área. Usando recta.")
            ruta_pts = [pA, pB]
            nodes = None
        else:
            registro.append("La recta A->B sale del área. Generando nodos seguros y buscando ruta alternativa.")
            nodes = generar_nodos_seguros(shape, num_nodos=NUM_NODOS, seed=42)
            def add_or_get_index(nodes_list, p, tol=1e-6):
                for idx, q in enumerate(nodes_list):
                    if euclid(p, q) < tol:
                        return idx
                nodes_list.append(p); return len(nodes_list)-1
            nodes = list(nodes)
            idx_A = add_or_get_index(nodes, pA)
            idx_B = add_or_get_index(nodes, pB)
            adj = construir_grafo(nodes, shape, k=K_NEIGHBORS)
            path_idx = dijkstra(adj, idx_A, idx_B)
            if path_idx is None:
                messagebox.showerror("Error", "No se encontró ruta alternativa con los nodos generados.")
                self.log_msg("\n".join(registro))
                return
            ruta_pts = [nodes[i] for i in path_idx]
            registro.append(f"Ruta encontrada con {len(ruta_pts)} puntos (incluyendo A y B).")

        # convertir ruta a ángulos (IK) y validar por reglas
        # cerrar reglas con parámetros actuales
        params = {k: float(v.get()) for k, v in self.entries.items()}
        params["usar_cond1"] = bool(self.var_cond1.get())
        params["usar_cond2"] = bool(self.var_cond2.get())
        regla1, regla2, regla3, regla4, regla5, es_postura_valida = make_rules(
            params["ri1"], params["rf1"], params["ri2"], params["rf2"],
            params["condicion1"], params["usar_cond1"],
            params["condicion2"], params["usar_cond2"]
        )

        ruta_angular = []
        ruta_angular_valida = True
        prev = None
        for p in ruta_pts:
            sols = inverse_kinematics(p[0], p[1], params["l1"], params["l2"])
            sols_validas = [s for s in sols if es_postura_valida(s[0], s[1])]
            if not sols_validas:
                ruta_angular_valida = False
                registro.append(f"Punto {p} sin solución válida de IK. Soluciones encontradas: {sols}")
                break
            # elegir solución continua
            if prev is None:
                chosen = sols_validas[0]
            else:
                best = None; bd = float('inf')
                for c in sols_validas:
                    d = abs(c[0]-prev[0]) + abs(c[1]-prev[1])
                    if d < bd:
                        bd = d; best = c
                chosen = best
            ruta_angular.append({"theta1_deg": float(chosen[0]), "theta2_deg": float(chosen[1]), "x": float(p[0]), "y": float(p[1])})
            prev = chosen
        if ruta_angular_valida:
            registro.append("Conversión a ángulos completa y válida.")
        else:
            registro.append("Conversión a ángulos fallida para al menos un waypoint; se guardará solo la ruta cartesiana.")

        # Guardar trayectoria JSON
        trayectoria_json = {
            "punto_inicial": {"x": float(pA[0]), "y": float(pA[1])},
            "punto_final": {"x": float(pB[0]), "y": float(pB[1])},
            "ruta_cartesiana": [{"x": float(x), "y": float(y)} for x, y in ruta_pts],
            "registro_experto": registro
        }
        if ruta_angular_valida:
            trayectoria_json["ruta_angular"] = ruta_angular
        tray_path = os.path.join(self.save_dir, "trayectoria_robot_angular.json")

        try:
            with open(tray_path, "w") as f:
                json.dump(trayectoria_json, f, indent=4)
            registro.append(f"Trayectoria guardada en {tray_path}")
        except Exception as e:
            registro.append(f"Error guardando trayectoria: {e}")

        # dibujar resultados en axes
        ax = self.ax
        ax.clear()
        ax.scatter(_workspace_points[:,0], _workspace_points[:,1], s=6, alpha=0.25, label="Workspace (muestras)")
        ax.plot([c[0] for c in _contour_xy], [c[1] for c in _contour_xy], 'r-', linewidth=2, label="Contorno (alpha)")
        # recta tentativa
        ax.plot([pA[0], pB[0]], [pA[1], pB[1]], color='gray', linestyle='--', linewidth=1, label="Recta A->B")
        # nodos si existen
        if nodes is not None:
            nodes_arr = np.array(nodes)
            ax.scatter(nodes_arr[:,0], nodes_arr[:,1], s=8, alpha=0.4, color='orange', label="Nodos seguros")
        # ruta
        ruta_x = [p[0] for p in ruta_pts]; ruta_y = [p[1] for p in ruta_pts]
        ax.plot(ruta_x, ruta_y, 'g-', linewidth=3, label="Ruta final")
        # marcar A,B
        ax.scatter([pA[0], pB[0]],[pA[1], pB[1]], color='blue', s=90, label="A,B")
        # puntos angulares opcional

        if ruta_angular_valida:
            ang_x = [pt["x"] for pt in ruta_angular]; ang_y = [pt["y"] for pt in ruta_angular]
            ax.scatter(ang_x, ang_y, s=30, c='cyan', edgecolors='k', label="Waypoints angulares")
        ax.set_aspect('equal','box'); ax.grid(True); ax.legend()
        self.canvas.draw()

        # log
        self.log_msg("\n".join(registro))
        messagebox.showinfo("Hecho", "Planificación completada. Revisa el log y los archivos generados.")

# ------------------------------
# Ejecutar aplicación
# ------------------------------
if __name__ == "__main__":
    # Verificar dependencias mínimas
    try:
        import shapely
        import alphashape
        import ezdxf
    except Exception as e:
        messagebox.showerror("Faltan librerías", f"Faltan librerías necesarias: {e}\nInstala shapely, alphashape, ezdxf con pip.")
        raise

    app = WorkspaceApp()
    app.mainloop()
