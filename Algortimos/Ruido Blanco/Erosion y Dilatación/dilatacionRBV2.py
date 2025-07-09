import cv2
import numpy as np
import matplotlib.pyplot as plt


def dilatar(ruidoBlanco,umbral,kernelDim,iteraciones):
    # Convertimos el ruido blanco en una imagen binaria (Si el valor es 0.5 o menos será un color y si no otro)
    ruido_binario = (ruidoBlanco > umbral).astype(np.uint8) * 255  # Escalamos a 0 y 255

    # Creamos un kernel para la dilatacion
    kernel = np.ones((kernelDim, kernelDim), np.uint8)  # Kernel 3x3

    # Aplicamos la erosión
    erosion = cv2.dilate(ruido_binario, kernel, iterations=iteraciones)

    return ruido_binario,erosion


'''# 0 - 0.25 Blancos
# 0.26 - 0.75 Grises
# 0.76 - 1 Negros'''

#DEGRADADO BASICO, CADA CASILLA SE AUMENTA EN UNA MEDIDA PROPORCIONAL AL TAMAÑO DEL PLANO
#Proximo: varios degradados conectados entre si

filas = 100
columnas = 100

modelo = np.zeros((filas, columnas))
ruido_blanco_suavizado = np.zeros((filas, columnas))

area = filas*columnas
incrementoMinimo = 1/area
incremento = 0
for fila in range(filas):
    for columna in range(columnas):
        #print('casilla: fila',fila,'columna',columna)
        ruido_blanco_suavizado[fila][columna] += incremento
        incremento += incrementoMinimo
        casillaActual = ruido_blanco_suavizado[fila][columna]
        #print(casillaActual)


binario, dilatacion= dilatar(ruido_blanco_suavizado,0.5,1,3)

#Indicamos valor maximo y valor minimo para establecer el blanco y el negro sin que esta se equilibre
plt.imshow(binario, cmap='gray', vmin=0, vmax=1)
plt.colorbar()
plt.show()

plt.imshow(dilatacion, cmap='gray', vmin=0, vmax=1)
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