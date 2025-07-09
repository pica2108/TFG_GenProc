import numpy as np
import matplotlib.pyplot as plt

'''
# 0 - 0.25 Blancos
# 0.26 - 0.75 Grises
# 0.76 - 1 Negros

Vamos a agrupar los coles por regiones de la cuadricula, pero distribuyendolos 
aleatoriamente segun el rango de grises que definen cada color.
'''

'''
Region del blanco --> (0,5) - (5,0) La suma siempre 5 o menos 
Region del Gris --> (0,10) - (10-0) La suma entre 6 y 10  
Region del Negro --> (5,10) - (10-5) La suma entre 11 y 15 
'''

def definirRegiones(filas,columnas):
    limiteRegionBlanco = filas/4 + columnas/4
    limiteRegionNegro = filas-filas/4 + columnas-columnas/4

    return limiteRegionBlanco,limiteRegionNegro
def obtenerRegion(fila,columna,limiteBlanco,limiteNegro):
    region = fila + columna
    if region <= limiteBlanco:
        return 'blanco'
    elif limiteBlanco<= region <= limiteNegro:
        return 'gris'
    else:
        return 'negro'

#Generamos una matriz 100x100 con valores aleatorios entre -1 y 1
filas = 100
columnas = 100
#ruido_blanco = np.random.uniform(0, 1, (filas, columnas))
ruido_blanco_suavizado = np.zeros((filas, columnas))

contBlancos = 0
contGrises = 0
contNegros = 0

limiteBlanco, limiteNegro = definirRegiones(filas,columnas)


for fila in range(0,filas):
    for columna in range(0,columnas):
        region = obtenerRegion(fila,columna,limiteBlanco,limiteNegro)
        if region == 'blanco':
            contBlancos+=1
            ruido_blanco_suavizado[fila][columna] = np.random.uniform(0,0.25)
        elif region == 'gris':
            contGrises += 1
            ruido_blanco_suavizado[fila][columna] = np.random.uniform(0.26, 0.75)
        elif region == 'negro':
            contNegros += 1
            ruido_blanco_suavizado[fila][columna] = np.random.uniform(0.76, 1)

#no se necesitan restricciones de rangos de gris ya que se establecen en el bucle, entre 0 y 1
plt.imshow(ruido_blanco_suavizado, cmap='gray_r')
plt.colorbar()
plt.show()


print(contBlancos,contGrises,contNegros)


'''Color Map Options:
'gray' 
'viridis'
'plasma'
'inferno'
'jet'
'coolwarm'

sufijo _r invierte el mapa de colores (jet_r)
'''