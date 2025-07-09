import cv2
import numpy as np
import matplotlib.pyplot as plt

#NO HACE NADA. NO HAY CAMBIOS
def dilatar(ruidoBlanco,umbral,kernelDim,iteraciones):
    ruido_binario = (ruidoBlanco > umbral).astype(np.uint8) * 255  # Escalamos a 0 y 255

    kernel = np.ones((kernelDim, kernelDim), np.uint8)  # Kernel 3x3

    erosion = cv2.dilate(ruido_binario, kernel, iterations=iteraciones)

    return ruido_binario,erosion



'''# 0 - 0.25 Blancos
# 0.26 - 0.75 Grises
# 0.76 - 1 Negros'''

#Cada casilla se establece segun la media de sus vecinos

filas = 100
columnas = 100

plano = np.random.uniform(0,1,(filas, columnas))


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
        #print(vecinos)
        mediaVecinos = 0
        for x,y in vecinos:
            mediaVecinos += plano[x][y]
        mediaVecinos = mediaVecinos/len(vecinos)
        plano[fila][columna] = mediaVecinos
        plano[fila][columna] += 0.05



#print(plano)

binario, planoDilatado = dilatar(plano,0.6,2,1)



plt.imshow(binario, cmap='gray_r', vmin=0, vmax=1)
plt.colorbar()
plt.show()

plt.imshow(planoDilatado, cmap='gray_r', vmin=0, vmax=1)
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