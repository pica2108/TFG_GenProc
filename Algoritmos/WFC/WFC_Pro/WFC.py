import math
import random
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def inicializarCuadricula(cuadricula,filas,columnas,colores):
    probabilidades = [0.9,0.1]
    for i in range(filas):
        for j in range(columnas):
            #color = random.choices(colores, weights=probabilidades, k=1)
            color = random.choice(colores)
            cuadricula[i][j] = [color]  # [color]

def verCuadricula(cuadricula,filas,columnas):
    for i in range(filas):
        print(cuadricula[i])
    print()


def obtenerVecinos(cuadricula,i,j,filas,columnas):
    casillasAdyacentes = []
    movs = ((0, 1), (0, -1), (1, 0), (-1, 0))
    for mov in movs:
        nuevaFila = i + mov[0]
        nuevaColumna = j + mov[1]
        if 0 <= nuevaFila < filas and 0 <= nuevaColumna < columnas:
            casillasAdyacentes.append((nuevaFila,nuevaColumna))
    return casillasAdyacentes

def obtenerTiles(cuadricula,filas,columnas,dimensionTiles):
    tiles = []
    tileId = 0
    for i in range(0, filas, dimensionTiles):
        for j in range(0, columnas, dimensionTiles):
            tile = [tileId]

            for x in range(i, min(i + dimensionTiles, filas)):
                filaTile = []
                for y in range(j, min(j + dimensionTiles, columnas)):
                    filaTile.append(cuadricula[x][y][0])

                tile.append(filaTile)
            print("TILE:",tile[0])
            tiles.append(tile)
            tileId += 1

    return tiles

'''Mira si cabe el tile en lo que queda de cuadricula, y coge el numero de filas que va a ocuapar el tile (Min 0, Max dimensionTile), coge las columnas comprobando lo mismo y las guarda
en filaTile. Al tener todas las filas las guarda en Tiles, y los primeros bucles saltan a la siguiente parte del cuadro donde cabe el siguiente tile'''

def verTiles(tiles):
    # Mostrar los tiles generados
    print("Tiles generados:")
    for t_idx, tile in enumerate(tiles):
        print(f"Tile {t_idx + 1}:")
        for fila in tile:
            print(fila)
        print()


def comprimirTiles(dimensionTablaAdyacencias):
    # Siguiente paso: Guardar por cada tile las posibles adyacencias segun su posicion. El marron no puede tener nada debajo a secas, POR ESO ERA
    tablaAdyacencias = [[0 for _ in range(dimensionTablaAdyacencias)] for _ in range(dimensionTablaAdyacencias)]
    k = 0
    for i in range(dimensionTablaAdyacencias):
        for j in range(dimensionTablaAdyacencias):
            tablaAdyacencias[i][j] = k
            k += 1
    print('Tabla de IDs:')
    for fila in tablaAdyacencias:
        print(fila)
    return tablaAdyacencias

def definirRepetidos(tiles,tablaAdyacencias,dim):
    listaColores = []
    for tile in tiles:
        if dim==1:
            listaColores.append(str(tile[1]))
        listaTile = ''
        for i in range(1,dim):
            listaTile = tile[i]+tile[i+1]
        numFinal = ''
        print(listaTile)
        for num in listaTile:
            numFinal += str(num)
            numFinal += '.'
        listaColores.append(numFinal)
    print(listaColores)

    iguales = []

    for i in range(len(listaColores)):
        for j in range(i + 1, len(listaColores)):  # Compara solo con los elementos siguientes para evitar duplicados
            if listaColores[i] == listaColores[j]:
                iguales.append((i,j))
    #print(iguales)

   #G
    mapeo = {}

    for a, b in iguales:
        valor_a = mapeo.get(a, tablaAdyacencias[a // len(tablaAdyacencias)][a % len(tablaAdyacencias)])
        mapeo[b] = valor_a

    for key, value in mapeo.items():
        tablaAdyacencias[key // len(tablaAdyacencias)][key % len(tablaAdyacencias)] = value

    print('-----------')
    for fila in tablaAdyacencias:
        print(fila)

    listaIDs = []
    for fila in tablaAdyacencias:
        for id in fila:
            listaIDs.append(id)
    #print(listaIDs)

    for i in range(len(tiles)):
        tiles[i][0] = listaIDs[i]
    #print(tiles)

    return tablaAdyacencias
    #G


def asignarAdyacenciasPorIDDireccional(dimensionTablaAdyacencias, tablaAdyacencias, tiles):
    # Diccionario para agrupar vecinos por ID único
    vecinosPorID = {}

    for i in range(dimensionTablaAdyacencias):
        for j in range(dimensionTablaAdyacencias):
            casilla = tablaAdyacencias[i][j]
            if casilla not in vecinosPorID:
                vecinosPorID[casilla] = {'id': casilla,'vecinos': {'arriba': [],'abajo': [],'izquierda': [],'derecha': []},'numVecinosSet': set()}  # Conjunto para vecinos únicos

            # Accedemos a los vecinos de la casilla actual
            direcciones = vecinosPorID[casilla]['vecinos']
            numVecinosSet = vecinosPorID[casilla]['numVecinosSet']  # Referencia al conjunto de vecinos únicos

            # Revisar cada dirección y añadir al conjunto correspondiente
            if i > 0:  # Arriba
                vecino = tablaAdyacencias[i - 1][j]
                direcciones['arriba'].append(vecino)
                direcciones['arriba'].sort()
                numVecinosSet.add(vecino)

            if i < dimensionTablaAdyacencias - 1:  # Abajo
                vecino = tablaAdyacencias[i + 1][j]
                direcciones['abajo'].append(vecino)
                direcciones['abajo'].sort()
                numVecinosSet.add(vecino)

            if j > 0:  # Izquierda
                vecino = tablaAdyacencias[i][j - 1]
                direcciones['izquierda'].append(vecino)
                direcciones['izquierda'].sort()
                numVecinosSet.add(vecino)

            if j < dimensionTablaAdyacencias - 1:  # Derecha
                vecino = tablaAdyacencias[i][j + 1]
                direcciones['derecha'].append(vecino)
                direcciones['derecha'].sort()
                numVecinosSet.add(vecino)

    vecinosTilesDireccionales = []

    # Convertir el conjunto en la cantidad total de vecinos únicos
    for entry in vecinosPorID.values():
        entry['numVecinos'] = len(entry.pop('numVecinosSet'))  # Contar elementos únicos
        vecinosTilesDireccionales.append(entry)

    # Mostrar vecinos direccionales
    for entry in vecinosTilesDireccionales:
        print(f"Tile ID: {entry['id']}, Vecinos: {entry['vecinos']}, Numero Vecinos: {entry['numVecinos']}")

    return vecinosTilesDireccionales


def main():

    filas = 6
    columnas = 6
    cuadricula = [[0 for _ in range(filas)] for _ in range(columnas)]
    colores = [0, 1]  # solo blanco y negro por ahora
    inicializarCuadricula(cuadricula,filas,columnas,colores)
    verCuadricula(cuadricula,filas,columnas)

    dimensionTiles = 2 # Tamaño de cada tile (ejemplo: 2x2)

    tiles = obtenerTiles(cuadricula, filas, columnas, dimensionTiles)
    verTiles(tiles)

    numTiles = len(tiles)
    dimensionTablaAdyacencias = int(numTiles ** (1 / 2))

    tablaAdyacencias = comprimirTiles(dimensionTablaAdyacencias)

    nuevaTablaAdyacencias = definirRepetidos(tiles, tablaAdyacencias,dimensionTiles)
    vecinosTilesDireccionales = asignarAdyacenciasPorIDDireccional(dimensionTablaAdyacencias, nuevaTablaAdyacencias, tiles)
    plt.imshow(cuadricula, cmap="gray")
    # plt.axis('off')  # Sin ejes para una visualización más limpia

    plt.show()

main()


