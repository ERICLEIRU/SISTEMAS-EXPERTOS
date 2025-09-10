# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 15:41:14 2025

@author: uriel
"""
import numpy as np
import matplotlib.pyplot as plt 

# X = np.arange(-2,5)

X = np.array([-2 , -1 , 0, 1, 2 ,3 , 4, 5])
n = len(X)
Y = X*2
W = np.arange(-2,6)
m = len(W)

YE = [W[c]*X for c in range(m)]

YdYE = [(Y-YE[c]) for c in range(m)]
YdYEpot2 = np.power(YdYE,2)

E = [(np.sum(YdYEpot2[c]))/(2*n) for c in range(m)]

plt.plot(W,E)
plt.show()
"""
YdYE = Y - YE  
YdYEpot2 = np.power(YdYE,2)



E = (np.sum(YdYEpot2))/2*n
"""