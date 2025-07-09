import math
import random
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

width = 20
height = 20
cuadricula = [[0 for _ in range(width)] for _ in range(height)]

for i in range(width):
    for j in range(height):
        cuadricula[i][j] = [None,['arena','agua','tierra','cesped']]

tiles = ['arena','agua','tierra','cesped']

markov = [(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1)]

def seleccionarCasilla(cuadricula):
    menorEntropia = 4
    casillaFinal = None

    y=0
    for fila in cuadricula:
        x=0
        for casilla in fila:
            if len(casilla[1]) <= menorEntropia and casilla[1][0]!=None:
                menorEntropia = len(casilla[1])
                casillaFinal = (y,x)
            x+=1
        y+=1
    return casillaFinal

def colapsarCasilla(cuadricula,casillaSeleccionada):
    casilla = cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]]
    eleccion = random.choice(casilla[1])
    cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][0] = eleccion
    cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][1] = [None]

def getMarkov(tile,markov):
    if tile == 'arena':
        return markov[0]
    elif tile == 'agua':
        return markov[1]
    elif tile == 'tierra':
        return markov[2]
    else:
        return markov[3]

def propagarCasilla(cuadricula,casillaSeleccionada,width,height,markov,tiles):
    casillasAdyacentes = []
    tile = cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][0]
    markovTile= getMarkov(tile,markov)
    movs = ((0,1),(0,-1),(1,0),(-1,0))
    fila = casillaSeleccionada[0]
    columna = casillaSeleccionada[1]
    for mov in movs:
        nuevaFila = fila + mov[0]
        nuevaColumna = columna + mov[1]
        if 0 <= nuevaFila < height and 0 <= nuevaColumna < width:
            casillasAdyacentes.append((nuevaFila,nuevaColumna))

    for casilla in casillasAdyacentes:
        cont = 0
        for opcion in markovTile:
            elemento = tiles[cont]
            if opcion == 0 and elemento in cuadricula[casilla[0]][casilla[1]][1]:
                cuadricula[casilla[0]][casilla[1]][1].remove(elemento)
            cont+=1


while True:
    time.sleep(0.01)
    casillaElegida = seleccionarCasilla(cuadricula)
    #print(casillaElegida)
    if casillaElegida is None:
        break
    colapsarCasilla(cuadricula, casillaElegida)
    propagarCasilla(cuadricula, casillaElegida, width, height, markov, tiles)
    #print(cuadricula)



for i in range(width):
    print()
    for j in range(height):
        print(cuadricula[i][j][0],end=" ")


#######  VISUALIZACION  ##########


''''# Imprimimos la cuadrícula colapsada
for fila in cuadricula:
    print([casilla[0] for casilla in fila])'''

# Diccionario para asignar un color a cada tipo de casilla
colores = {'arena': (194, 178, 128), 'agua': (64, 164, 223), 'tierra': (139, 69, 19), 'cesped': (45,87,44)}

# Creamos una matriz de colores para la visualización
imagen = np.zeros((height, width, 3), dtype=np.uint8)

# Asignamos colores a cada casilla en la cuadrícula colapsada
for i in range(height):
    for j in range(width):
        tile = cuadricula[i][j][0]
        if tile in colores:
            imagen[i, j] = colores[tile]

# Mostramos la imagen con matplotlib
plt.imshow(imagen)
plt.axis('off')  # Sin ejes para una visualización más limpia
plt.show()