import random

import numpy as np
import matplotlib.pyplot as plt

'''# 0 - 0.25 Blancos
# 0.26 - 0.75 Grises
# 0.76 - 1 Negros'''

#Cada casilla cogera el color de uno de sus vecinos y lo incrementara o disminuira aleatoriamente

filas = 100
columnas = 100

plano = np.zeros((filas, columnas))
#plano = np.random.uniform(0,1,(filas,columnas))


def esPosicionValida(fila,columna,filas,columnas):
    return 0 <= fila < filas and 0 <= columna < columnas
def calcularVecinos(fila,columna,filas,columnas):
    direcciones = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    vecinos = []

    for f,c in direcciones:
        filaNueva = fila + f
        columnaNueva = columna + c
        if esPosicionValida(filaNueva,columnaNueva,filas,columnas):
            vecinos.append((filaNueva,columnaNueva))

    return vecinos

for fila in range(filas):
    for columna in range(columnas):
        vecinos = calcularVecinos(fila,columna,filas,columnas)
        vex = random.randint(0,len(vecinos)-1)
        fx,yx = vecinos[vex]
        print(plano[fx][yx])
        incremento = np.random.uniform(0, 0.3)
        plano[fila][columna] = plano[fx][yx] + incremento
        #plano[fila][columna] += np.random.uniform(-0.2, 0.2)



#print(plano)


plt.imshow(plano, cmap='gray', vmin=0, vmax=1)
plt.colorbar()
plt.show()


'''Color Map Options:
'gray' 
'viridis'
'plasma'
'inferno'
'jet'
'coolwarm'

sufijo _r invierte el mapa de colores (jet_r)
'''