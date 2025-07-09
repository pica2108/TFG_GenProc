import numpy as np
import matplotlib.pyplot as plt

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


plt.imshow(ruido_blanco_suavizado, cmap='gray', vmin=0, vmax=1)
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