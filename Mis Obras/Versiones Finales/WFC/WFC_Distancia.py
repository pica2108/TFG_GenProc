import math
import random
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

width = 100
height = 100
cuadricula = [[0 for _ in range(width)] for _ in range(height)]

for i in range(width):
    for j in range(height):
        cuadricula[i][j] = ['mar', False]




def inicializarCosta(cuadricula, height, width):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)

    casilla = (x,y)
    cuadricula[casilla[0]][casilla[1]][0] = 'arena'
    #colapsarCasilla(cuadricula, casilla, limiteAgua)
    #propagarCosta(cuadricula, height, width, areaCosta)

def propagarCosta(cuadricula, height, width,areaCosta):
    casillas = []
    x,y = buscarCosta(cuadricula,width,height)
    for _ in range(areaCosta):
        vecinosCasilla = vecinos(x,y,height,width)
        x2, y2 = random.choice(vecinosCasilla)
        while(cuadricula[x2][y2][0] != 'mar'):
            x2,y2 = random.choice(vecinosCasilla)
        cuadricula[x2][y2][0] = 'arena'
        casillas.append((x2,y2))
        y,x = buscarCosta(cuadricula,width,height)
    return casillas


# Busca una casilla adecuada para continuar la expansión de la costa

def distancia_al_mar(cuadricula, casilla, width, height):
    x,y = casilla
    min_dist = float('inf')
    for i in range(height):
        for j in range(width):
            if cuadricula[i][j][0] == 'mar':
                dist = math.sqrt((x - j) ** 2 + (y - i) ** 2)
                min_dist = min(min_dist, dist)
    return min_dist



def buscarCosta(cuadricula, width, height):
    celdas_costa = []
    for y in range(height):
        for x in range(width):
            if cuadricula[y][x][0] != 'mar' and any(
                    cuadricula[ny][nx][0] == 'mar' for ny, nx in vecinos(x, y, width, height)):
                celdas_costa.append((y, x))
    return random.choice(celdas_costa) if celdas_costa else (0, 0)


# Obtiene vecinos válidos dentro de la cuadrícula


def vecinos(y, x, width, height):
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0),(1,1),(1,-1),(-1,1)]
    return [(y + dy, x + dx) for dx, dy in direcciones if 0 <= x + dx < width and 0 <= y + dy < height]


def vecinos2(x, y, width, height):
    vecino = []
    movs = ((0, 1), (0, -1), (1, 0), (-1, 0))
    fila = x
    columna = y
    for mov in movs:
        nuevaFila = fila + mov[0]
        nuevaColumna = columna + mov[1]
        if 0 <= nuevaFila < height and 0 <= nuevaColumna < width:
            vecino.append((nuevaFila, nuevaColumna))
    return vecinos


# Selecciona la casilla con menor entropía

'''def seleccionarCasilla(cuadricula, height, width):
    menorEntropia = len(tiles)
    casillaFinal = None
    for y in range(height):
        for x in range(width):
            if len(cuadricula[y][x][1]) < menorEntropia and cuadricula[y][x][1][0] is not None:
                menorEntropia = len(cuadricula[y][x][1])
                casillaFinal = (y, x)

    if menorEntropia == len(tiles):
        casillaFinal = buscarCosta(cuadricula, width, height)
    return casillaFinal'''


# Colapsa una casilla seleccionada

def colapsarCasilla(cuadricula, casillaSeleccionada, height, width):
    max_distancia = math.sqrt(height ** 2 + width ** 2)  # Distancia máxima posible en la cuadrícula
    distancia = distancia_al_mar(cuadricula, casillaSeleccionada, width, height)
    proporcion = distancia / max_distancia  # Normalizar la distancia entre 0 y 1

    y, x = casillaSeleccionada

    if proporcion <= 0.05:
        cuadricula[y][x][0] = 'arena'
    elif proporcion <= 0.10:
        cuadricula[y][x][0] = 'cesped'
    elif proporcion <= 0.15:
        cuadricula[y][x][0] = 'cesped2'
    elif proporcion <= 0.25:
        cuadricula[y][x][0] = 'piedra'
    elif proporcion <= 0.30:
        cuadricula[y][x][0] = 'piedra'
    else:
        cuadricula[y][x][0] = 'piedra'

    cuadricula[y][x][1] = True


############ INICIALIZACIÓN ###########

extensionCosta = random.randint(2,8)
areaCosta = int((height * width) * (extensionCosta/10))

inicializarCosta(cuadricula, height, width)
casillas = propagarCosta(cuadricula,height,width,areaCosta)

print("Fase 2")
while(len(casillas)!= 0):
    j,i = random.choice(casillas)
    if cuadricula[j][i][0] == 'arena' and cuadricula[j][i][1] == False:
        casilla = (j,i)
        casillas.remove((j,i))
        colapsarCasilla(cuadricula, casilla,height,width)


####### VISUALIZACIÓN ##########
colores = {'arena': (194, 178, 128), 'piedra': (50, 50, 50), 'tierra': (139, 69, 19), 'cesped': (45, 87, 44), 'tierra2': (100, 50, 20), 'cesped2': (25, 60, 25), 'mar': (50, 0, 223)}

imagen = np.zeros((height, width, 3), dtype=np.uint8)
for i in range(height):
    for j in range(width):
        tile = cuadricula[i][j][0]
        if tile in colores:
            imagen[i, j] = colores[tile]

plt.imshow(imagen)
plt.axis('off')
plt.show()
