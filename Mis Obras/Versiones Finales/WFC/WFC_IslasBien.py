import math
import random
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

inicio = time.time()
width = 150
height = 150
cuadricula = [[0 for _ in range(width)] for _ in range(height)]

for i in range(width):
    for j in range(height):
        cuadricula[i][j] = ['mar',['tierra','cesped','agua']]

tiles = ['tierra','cesped','agua']

#RESTRICCIONES

#Modificamos las restricciones para que solo la arena este con el agua, y solo el la tierra esté con el cesped
#La tierra puede llevar cesped y agua

markov = [(1,1,0),(1,1,1),(0,1,1)]

 #      Tierra    Cesped      Agua


def obtenerBordes(width, height):
    bordes = []

    # Definir los márgenes como porcentaje del tamaño total
    margen_y_superior = round(height * 0.09)  # 9% superior
    margen_y_inferior = round(height * 0.05)  # 5% inferior
    margen_x_izquierda = round(width * 0.08)  # 8% izquierda
    margen_x_derecha = round(width * 0.04)  # 4% derecha

    for y in range(height):
        for x in range(width):
            if y < margen_y_superior or y >= height - margen_y_inferior or x < margen_x_izquierda or x >= width - margen_x_derecha:
                bordes.append((y, x))

    return bordes

########

def inicializarIsla(cuadricula, height, width,limiteAgua,markov,tiles):
    x = random.randint(0,width-1)
    y = random.randint(0,height-1)
    casilla = (y,x)
    cuadricula[casilla[0]][casilla[1]][0] = 'tierra'
    colapsarCasilla(cuadricula,casilla,limiteAgua)
    propagarCasilla(cuadricula,casilla,width,height,markov,tiles)


def buscarIsla(cuadricula):
    celdas_Isla = []
    for y in range(height):
        for x in range(width):
            if cuadricula[y][x][0] != 'mar' and any(
                    cuadricula[ny][nx][0] == 'mar' for ny, nx in vecinos(x, y, width, height)):
                celdas_Isla.append((y, x))
    return random.choice(celdas_Isla) if celdas_Isla else (0, 0)

def vecinos(x, y, width, height):
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [(y + dy, x + dx) for dx, dy in direcciones if 0 <= x + dx < width and 0 <= y + dy < height]


def seleccionarCasilla(cuadricula,height,width,numMaxIslas,bordes):
    menorEntropia = len(tiles)
    casillaFinal = None

    y=0
    for fila in cuadricula:
        x=0
        for casilla in fila:
            if len(casilla[1]) < menorEntropia and casilla[1][0]!=None and (x,y) not in bordes:
                menorEntropia = len(casilla[1])
                casillaFinal = (y,x)
            x+=1
        y+=1
    if menorEntropia == len(tiles):
        if numMaxIslas[0] > 0:
            x2 = random.randint(0, width - 1)
            y2 = random.randint(0, height - 1)
            numMaxIslas[0] -=1
            casillaFinal = (y2,x2)
        else:
            casillaFinal = buscarIsla(cuadricula)
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
    if tile == 'tierra':
        return markov[0]
    elif tile == 'cesped':
        return markov[1]
    else:
        return markov[2]

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

def limpiarIslasPeques(cuadricula, width, height):
    esquinas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Esquinas diagonales
    adyacentes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Adyacentes no diagonales (arriba, abajo, izquierda, derecha)

    for fila in range(height):
        for columna in range(width):
            tieneMarEnEsquinas = True
            if cuadricula[fila][columna][0] == (0,0,0):
                cuadricula[fila][columna][0] = 'arena'
            # Verificar si las cuatro esquinas de la casilla son "mar"
            for mov in esquinas:
                nuevaFila = fila + mov[0]
                nuevaColumna = columna + mov[1]
                if not (0 <= nuevaFila < height and 0 <= nuevaColumna < width) or cuadricula[nuevaFila][nuevaColumna][0] != 'mar':
                    tieneMarEnEsquinas = False
                    break

            # Si todas las esquinas son "mar", convertir la casilla y las adyacentes no diagonales en "mar"
            if tieneMarEnEsquinas:
                cuadricula[fila][columna][0] = 'mar'  # Convertir la casilla en "mar"

                # Convertir las casillas adyacentes no diagonales en "mar"
                for mov in adyacentes:
                    nuevaFila = fila + mov[0]
                    nuevaColumna = columna + mov[1]
                    if 0 <= nuevaFila < height and 0 <= nuevaColumna < width:
                        cuadricula[nuevaFila][nuevaColumna][0] = 'mar'

##### FUNCIONES DE CALIDAD #########

def verificarBordes(cuadricula, width, height,bordes): #Nos indica si las islas estan rodeadas completamente por mar
    contador = 0
    area = width * height
    for (x,y) in bordes:
        if cuadricula[x][y][0] != 'mar':
            contador += 1
    aux = (contador/area)*100
    superBordes = round(aux,2)
    return superBordes #Maxima

def verificarArena(cuadricula, width, height): #cantidad de arena que esta conectada al mar
    contador = 0
    contCasilla = 0
    area = width * height
    for fila in range(height):
        for columna in range(width):
            if cuadricula[fila][columna][0] != 'arena' and cuadricula[fila][columna][0] != 'mar':
                vecinosCasilla = vecinos(fila,columna,width,height)
                contCasilla += 1
                for (x,y) in vecinosCasilla:
                    if cuadricula[y][x][0] == 'mar':
                        contador += 1
                        break
    tierraAlMar = 100 - round((contador / contCasilla),2) * 100
    return tierraAlMar #2

def contrastarBiomas(cuadricula, width, height,extensionEsperada):
    info = []
    agua = 0
    tierra = 0
    cesped = 0
    mar = 0
    area = width * height
    for fila in range(height):
        for columna in range(width):
            if cuadricula[fila][columna][0] == 'agua':
                agua += 1
            elif cuadricula[fila][columna][0] == 'tierra':
                tierra += 1
            elif cuadricula[fila][columna][0] == 'cesped':
                cesped += 1
            elif cuadricula[fila][columna][0] == 'mar':
                mar += 1

    pMar = (round(mar/area,2)*100)
    superficie  = area - mar
    pAgua = round((agua/superficie)*100,2)
    pTierra = round((tierra/superficie)*100,2)
    pCesped = round((cesped/superficie)*100,2)
    superficieEsperada = area*extensionEsperada
    diferencia = superficieEsperada / superficie
    aux = abs(1-diferencia)
    pSuperficieEsperada = round((1 - aux) * 100, 2)

    info.append(pMar) #2
    info.append(pAgua) #1
    info.append(pTierra) #1
    info.append(pCesped) #1
    info.append(pSuperficieEsperada) #3

    return info


def funcionCalidad(tiempo, superBordes, arenaConectada, pAgua, pTierra, pCesped, pSuperEsperada,penalizacionLineas,longitud_actual,totalLineas,umbral):
    # Penalización extrema si demasiada isla toca el borde
    if superBordes > 15:
        print(f"❌ Penalización máxima: demasiada isla tocando el borde ({superBordes}%). Puntuación = 0")
        return 0

    # Penalización progresiva por tocar bordes (hasta 30 puntos de penalización)
    penalizacionBordes = round(min(superBordes * 10, 15), 2)
    print(f"🚧 Penalización por isla en los bordes ({superBordes}% de la isla): -{penalizacionBordes} puntos")

    # Penalización por diferencia entre tierra y césped
    diferenciaTierraCesped = abs(pTierra*2 - pCesped)
    penalizacionTierraCesped = round(min(diferenciaTierraCesped * 0.5, 15), 2)  # Máx. 15 puntos
    print(f"🌱 Penalización por diferencia tierra/césped ({pTierra*1.5}% vs {pCesped}%): -{penalizacionTierraCesped} puntos")

    # Penalización por tierra conectada del mar
    penalizacionArena = round(max(0, 100 - arenaConectada) * 0.3, 2)  # Máx. 30 puntos
    print(f"🏝️ Penalización por arena no conectada al mar ({arenaConectada}% conectada): -{penalizacionArena} puntos")


    #Penalizacion por islas irregulares
    print(f"📐 Penalización por líneas rectas de arena:")
    print(f"    ➤ Longitud minima: {umbral}")
    print(f"    ➤ Líneas encontradas: {totalLineas}")
    print(f"    ➤ Longitud total de líneas: {longitud_actual}")
    print(f"    ➤ Penalización aplicada: -{penalizacionLineas} puntos")


    # Penalización por desviación de la superficie esperada
    penalizacionSuperficie = round((100 - pSuperEsperada) * 0.15, 2)  # Máx. 15 puntos
    print(f"📏 Penalización por diferencia en superficie esperada ({pSuperEsperada}% logrado): -{penalizacionSuperficie} puntos")

    # Penalización por tiempo de ejecución
    penalizacionTiempo = round(min(tiempo * 2, 20), 2)  # Penaliza 2 puntos por segundo, hasta un máximo de 20 puntos
    print(f"⏳ Penalización por tiempo de ejecución ({tiempo:.2f}s): -{penalizacionTiempo} puntos")

    # Cálculo de la puntuación final
    puntuacion = 100 - (penalizacionBordes + penalizacionTierraCesped + penalizacionArena + penalizacionLineas + penalizacionSuperficie + penalizacionTiempo)

    # No permitir puntuaciones negativas
    puntuacion = max(0, round(puntuacion, 2))
    print(f"✅ Puntuación final: {puntuacion} puntos")

    return puntuacion


def penalizarLineasArena(cuadricula, width, height):
    umbral = max(6, int(min(width, height) * 0.1))  # 8% del tamaño mínimo, mínimo 5
    total_lineas = 0
    longitud_total = 0

    # Revisamos filas (horizontales)
    for y in range(height):
        longitud_actual = 0
        for x in range(width):
            if cuadricula[y][x][0] == 'arena':
                longitud_actual += 1
            else:
                if longitud_actual >= umbral:
                    total_lineas += 1
                    longitud_total += longitud_actual
                longitud_actual = 0
        # Final de la fila
        if longitud_actual >= umbral:
            total_lineas += 1
            longitud_total += longitud_actual

    # Revisamos columnas (verticales)
    for x in range(width):
        longitud_actual = 0
        for y in range(height):
            if cuadricula[y][x][0] == 'arena':
                longitud_actual += 1
            else:
                if longitud_actual >= umbral:
                    total_lineas += 1
                    longitud_total += longitud_actual
                longitud_actual = 0
        # Final de la columna
        if longitud_actual >= umbral:
            total_lineas += 1
            longitud_total += longitud_actual

    # Penalización basada en cantidad y longitud total de líneas
    penalizacion = round((total_lineas * longitud_total) / (width * height),7)*2000
    penalizacion = min(15,penalizacion)


    return penalizacion,longitud_total,total_lineas,umbral


############INICIALIZACION###########

extensionTierra = 0.3
areaTierra = int((height*width)*extensionTierra)


#### RESTRICCIONES CONCRETAS ######

areaAgua = 0.4 #Indica el maximo porcentaje de agua que podra haber en la costa
limiteAgua = [areaTierra * areaAgua, 0]
bordes = obtenerBordes(width,height)
##########
numMaxIslasExtra = [6]
areaIsla = areaTierra//(numMaxIslasExtra[0]+1)
inicializarIsla(cuadricula, height, width,limiteAgua,markov,tiles)
for _ in range(numMaxIslasExtra[0]+1):
    for _ in range(areaIsla):
        casillaElegida = seleccionarCasilla(cuadricula,height,width,numMaxIslasExtra,bordes)
        #print(numMaxIslasExtra,end="\n")
        #print(casillaElegida)
        if casillaElegida is None:
            break

        colapsarCasilla(cuadricula, casillaElegida,limiteAgua)
        propagarCasilla(cuadricula, casillaElegida, width, height, markov, tiles)
        #print(cuadricula)


#### EXTRAS ####

fin = time.time()
tiempoEjec = fin - inicio
print("Tiempo de ejecucion:",round(tiempoEjec,4),end="s\n")
limpiarIslasPeques(cuadricula,width,height)

superBordes = verificarBordes(cuadricula,width,height,bordes)
tierraAlMar = verificarArena(cuadricula,width,height)
infoBiomas = contrastarBiomas(cuadricula,width,height,extensionTierra)

pMar = infoBiomas[0]
pAgua = infoBiomas[1]
pTierra = infoBiomas[2]
pCesped = infoBiomas[3]
pSuperEsperada = infoBiomas[4]

puntuacionLineas,longitud_actual,totalLineas,umbral= penalizarLineasArena(cuadricula, width, height)
puntuacion = funcionCalidad(tiempoEjec,superBordes,tierraAlMar,pAgua,pTierra,pCesped,pSuperEsperada,puntuacionLineas,longitud_actual,totalLineas,umbral)




#######  VISUALIZACION  ##########


''''# Imprimimos la cuadrícula colapsada
for fila in cuadricula:
    print([casilla[0] for casilla in fila])'''

# Diccionario para asignar un color a cada tipo de casilla
colores = {'arena': (194, 178, 128), 'agua': (64, 164, 223), 'tierra': (139, 69, 19), 'cesped': (45,87,44), 'mar': (50, 0, 223), 'negro':(0,0,0)}

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
plt.title(f"Islas generadas por Colapso de Onda")
plt.axis('on')  # Sin ejes para una visualización más limpia
plt.show()