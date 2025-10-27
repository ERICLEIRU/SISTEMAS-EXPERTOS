import random
import tkinter as tk
from tkinter import messagebox

# Datos
personajes = ["Laura", "Carlos", "Ana", "Marta", "Luis"]
armas = ["Cuchillo", "Cuerda", "Pistola", "Veneno", "Hacha"]
lugares = ["Bosque", "Callejón", "Mansión", "Biblioteca", "Tren"]

# Solución aleatoria
solucion = {
    "persona": random.choice(personajes),
    "arma": random.choice(armas),
    "lugar": random.choice(lugares)
}

# Genera pistas lógicas
def generar_pistas_logicas(sol):
    pistas = []

    # Personas
    no_personas = [p for p in personajes if p != sol["persona"]]
    pistas.append(f"El asesino NO es: {', '.join(random.sample(no_personas, 2))}.")
    pistas.append(f"El asesino es uno de: {sol['persona']} o {random.choice(no_personas)}.")

    # Armas
    no_armas = [a for a in armas if a != sol["arma"]]
    pistas.append(f"El arma NO es: {random.choice(no_armas)} ni {random.choice(no_armas)}.")
    pistas.append(f"El arma usada fue veneno o cuerda." if sol["arma"] in ["Veneno", "Cuerda"] else
                 f"El arma usada fue {sol['arma']} o {random.choice(no_armas)}.")

    # Lugares
    no_lugares = [l for l in lugares if l != sol["lugar"]]
    pistas.append(f"El crimen NO ocurrió en: {random.choice(no_lugares)}.")
    pistas.append(f"El lugar del crimen es el {sol['lugar']} o {random.choice(no_lugares)}.")

    random.shuffle(pistas)
    return pistas[:6]  # Limitamos a 6 pistas

pistas = generar_pistas_logicas(solucion)

def deducir_asesino(persona, arma, lugar):
    return persona == solucion["persona"] and arma == solucion["arma"] and lugar == solucion["lugar"]

class ClueApp:
    def __init__(self, master):
        self.master = master
        master.title("Juego de Clue - Asesino Serial")

        tk.Label(master, text="🔍 Pistas:").grid(row=0, column=0, columnspan=2, sticky="w")

        # Mostrar pistas en Labels
        for i, pista in enumerate(pistas):
            tk.Label(master, text=f"- {pista}").grid(row=i+1, column=0, columnspan=2, sticky="w")

        # Selección jugador
        tk.Label(master, text="Selecciona al sospechoso:").grid(row=7, column=0, sticky="w")
        self.persona_var = tk.StringVar(master)
        self.persona_var.set(personajes[0])
        tk.OptionMenu(master, self.persona_var, *personajes).grid(row=7, column=1, sticky="w")

        tk.Label(master, text="Selecciona el arma:").grid(row=8, column=0, sticky="w")
        self.arma_var = tk.StringVar(master)
        self.arma_var.set(armas[0])
        tk.OptionMenu(master, self.arma_var, *armas).grid(row=8, column=1, sticky="w")

        tk.Label(master, text="Selecciona el lugar:").grid(row=9, column=0, sticky="w")
        self.lugar_var = tk.StringVar(master)
        self.lugar_var.set(lugares[0])
        tk.OptionMenu(master, self.lugar_var, *lugares).grid(row=9, column=1, sticky="w")

        # Botón para acusar
        self.btn_acusar = tk.Button(master, text="Acusar", command=self.acusar)
        self.btn_acusar.grid(row=10, column=0, columnspan=2, pady=10)

    def acusar(self):
        persona = self.persona_var.get()
        arma = self.arma_var.get()
        lugar = self.lugar_var.get()

        if deducir_asesino(persona, arma, lugar):
            messagebox.showinfo("Resultado", f"¡Correcto! {persona} es el asesino serial con el {arma} en el {lugar} 🕵️‍♂️🔪")
        else:
            messagebox.showerror("Resultado", f"Incorrecto. {persona} no es el asesino con ese arma y lugar.\nIntenta otra combinación.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClueApp(root)
    root.mainloop()
