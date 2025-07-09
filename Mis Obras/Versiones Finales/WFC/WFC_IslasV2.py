import math
import random
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

width = 50
height = 50
cuadricula = [[0 for _ in range(width)] for _ in range(height)]

for i in range(width):
    for j in range(height):
        cuadricula[i][j] = ['mar',['arena','tierra','cesped','agua','piedra']]

tiles = ['arena','tierra','cesped','agua','piedra']

#RESTRICCIONES

#Modificamos las restricciones para que solo la arena este con el agua, y solo el la tierra esté con el cesped
#La tierra puede llevar cesped y agua

markov = [(1,1,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,1,1),(0,0,0,0,1)]
 #            Arena     Tierra      Cesped      Agua        piedra
########

def primeraSeleccion(width,height):
    x = random.randint(0,width-1)
    y = random.randint(0,height-1)

    casillaFinal = (y,x)
    return casillaFinal
def seleccionarCasilla(cuadricula,width,height):
    menorEntropia = len(tiles)
    casillaFinal = None

    y=0
    for fila in cuadricula:
        x=0
        for casilla in fila:
            if casilla[1] and len(casilla[1]) <= menorEntropia and casilla[1][0]!=None:
                menorEntropia = len(casilla[1])
                casillaFinal = (y,x)
            x+=1
        y+=1
        if menorEntropia == len(tiles):
            return primeraSeleccion(width,height)
    return casillaFinal

def colapsarCasilla(cuadricula,casillaSeleccionada,limiteDeAgua):
    casilla = cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]]
    eleccion = random.choice(casilla[1])
    if eleccion != 'agua':
        cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][0] = eleccion
        cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][1] = [None]
    if limiteDeAgua[1] < limiteDeAgua[0]:
        limiteDeAgua[1] += 1
        cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][0] = eleccion
        cuadricula[casillaSeleccionada[0]][casillaSeleccionada[1]][1] = [None]


def getMarkov(tile,markov):
    if tile == 'arena':
        return markov[0]
    if tile == 'tierra':
        return markov[1]
    elif tile == 'cesped':
        return markov[2]
    elif tile == 'agua':
        return markov[3]
    else:
        return markov[4]

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
        if cuadricula[casilla[0]][casilla[1]][0] == 'mar':
            cuadricula[casilla[0]][casilla[1]][0] = 'arena'
        cont = 0
        for opcion in markovTile:
            elemento = tiles[cont]
            if opcion == 0 and elemento in cuadricula[casilla[0]][casilla[1]][1]:
                cuadricula[casilla[0]][casilla[1]][1].remove(elemento)
            cont+=1



############INICIALIZACION###########

extensionCosta = 0.3333
areaCosta = int((height*width)*extensionCosta)

#### RESTRICCIONES CONCRETAS ######

areaAgua = 0.3 #Indica el maximo porcentaje de agua que podra haber en la costa
limiteAgua = [areaCosta * areaAgua, 0]

##########
for i in range(areaCosta):
    if i==0:
        casillaElegida = primeraSeleccion(width,height)
    else:
        casillaElegida = seleccionarCasilla(cuadricula,width,height)
    #print(casillaElegida)
    if casillaElegida is None:
        break

    colapsarCasilla(cuadricula, casillaElegida,limiteAgua)
    propagarCasilla(cuadricula, casillaElegida, width, height, markov, tiles)
    #print(cuadricula)

#######  VISUALIZACION  ##########


# Diccionario para asignar un color a cada tipo de casilla
colores = {'arena': (194, 178, 128), 'agua': (64, 164, 223), 'tierra': (139, 69, 19), 'cesped': (45,87,44), 'mar': (50, 0, 223),'piedra': (100, 100, 100)}

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