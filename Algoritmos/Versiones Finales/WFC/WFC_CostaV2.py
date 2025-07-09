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
        cuadricula[i][j] = ['mar', ['tierra','tierra2','cesped','cesped2','agua']]

tiles = ['tierra','tierra2','cesped','cesped2', 'agua']

# RESTRICCIONES
markov = [(1,1,0,1,0),(1,1,0,1,0), (1,0,1,1,1),(1,0,1,1,1), (0,0,1,1,1)]
#          tierra       tierra2      cesped      cesped2       agua
# Inicializa la costa desde un borde aleatorio
#markov = [(1,1,0,1,0),(1,1,0,1,0), (1,0,1,1,1),(1,0,1,1,1), (0,0,1,1,1)]

def inicializarCosta(cuadricula, height, width, limiteAgua, markov, tiles):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    lados = [(height-1,width-1),(y, 0), (x, 0), (0, y), (0, x), (0, 0), (0, width - 1), (width - 1, 0), (0, height - 1), (height - 1, 0),(width-1,x),(x,width-1),(height-1,y),(y,height-1)]
    casilla = random.choice(lados)
    cuadricula[casilla[0]][casilla[1]][0] = 'tierra'
    #colapsarCasilla(cuadricula, casilla, limiteAgua)
    propagarCasilla(cuadricula, casilla, width, height, markov, tiles)

def obtenerBordes(width, height):
    bordes = []

    for y in range(height):
        for x in range(width):
            if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                bordes.append((y, x))

    return bordes
def distanciaACosta(cuadricula, casilla, width, height):
    x,y = casilla
    min_dist = float('inf')
    for i in range(height):
        for j in range(width):
            if cuadricula[i][j][0] == 'arena' :
                dist = math.sqrt((x - j) ** 2 + (y - i) ** 2)
                min_dist = min(min_dist, dist)
    return min_dist

def skinMar(cuadricula,width,height,areaCosta):
    for y in range(height):
        for x in range(width):
            if cuadricula[y][x][0] == 'mar':
                casilla = (y,x)
                if distanciaACosta(cuadricula, casilla, width, height) >= areaCosta//250:
                    cuadricula[y][x][0] = 'marProfundo'

# Busca una casilla adecuada para continuar la expansión de la costa

def buscarCosta(cuadricula, width, height):
    celdas_costa = []
    for y in range(height):
        for x in range(width):
            if cuadricula[y][x][0] != 'mar' and any(
                    cuadricula[ny][nx][0] == 'mar' for ny, nx in vecinos(x, y, width, height)):
                celdas_costa.append((y, x))
    return random.choice(celdas_costa) if celdas_costa else (0, 0)


# Obtiene vecinos válidos dentro de la cuadrícula

def vecinos(x, y, width, height):
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [(y + dy, x + dx) for dx, dy in direcciones if 0 <= x + dx < width and 0 <= y + dy < height]


# Selecciona la casilla con menor entropía

def seleccionarCasilla(cuadricula, height, width):
    menorEntropia = len(tiles)
    casillaFinal = None
    for y in range(height):
        for x in range(width):
            if len(cuadricula[y][x][1]) < menorEntropia and cuadricula[y][x][1][0] is not None:
                menorEntropia = len(cuadricula[y][x][1])
                casillaFinal = (y, x)

    if menorEntropia == len(tiles):
        casillaFinal = buscarCosta(cuadricula, width, height)
    return casillaFinal


# Colapsa una casilla seleccionada

def colapsarCasilla(cuadricula, casillaSeleccionada, limiteDeAgua):
    y, x = casillaSeleccionada
    eleccion = random.choice(cuadricula[y][x][1])
    if eleccion != 'agua':
        cuadricula[y][x][0] = eleccion
        cuadricula[y][x][1] = [None]
    if limiteDeAgua[1] < limiteDeAgua[0]:
        limiteDeAgua[1] += 1
        cuadricula[y][x][0] = eleccion
        cuadricula[y][x][1] = [None]


# Propaga la influencia de la casilla colapsada a sus vecinos

def propagarCasilla(cuadricula, casillaSeleccionada, width, height, markov, tiles):
    y, x = casillaSeleccionada
    tile = cuadricula[y][x][0]
    markovTile = getMarkov(tile, markov)
    for ny, nx in vecinos(x, y, width, height):
        if cuadricula[ny][nx][0] == 'mar':
            cuadricula[ny][nx][0] = 'arena'
        for i, opcion in enumerate(markovTile):
            if opcion == 0 and tiles[i] in cuadricula[ny][nx][1]:
                cuadricula[ny][nx][1].remove(tiles[i])


def getMarkov(tile, markov):
    return markov[0] if tile == 'tierra' else markov[1] if tile == 'tierra2' else markov[2] if tile == 'cesped' else markov[3] if tile == 'cesped2' else markov[4]


###### CALIDAD ########

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
    return tierraAlMar

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
            elif cuadricula[fila][columna][0] == 'tierra' or cuadricula[fila][columna][0] == 'tierra2':
                tierra += 1
            elif cuadricula[fila][columna][0] == 'cesped' or cuadricula[fila][columna][0] == 'cesped2':
                cesped += 1
            elif cuadricula[fila][columna][0] == 'mar' or cuadricula[fila][columna][0] == 'marProfundo':
                mar += 1

    pMar = (round(mar/area,2)*100)
    superficie  = area - mar
    print(superficie)
    pAgua = round((agua/superficie)*100,2)
    pTierra = round((tierra/superficie)*100,2)
    pCesped = round((cesped/superficie)*100,2)
    superficieEsperada = area*extensionEsperada
    print(superficieEsperada)
    diferencia = superficieEsperada / superficie
    print(diferencia)
    aux = abs(1-diferencia)
    pSuperficieEsperada = round((1 - aux) * 100, 2)
    print(pSuperficieEsperada)
    info.append(pMar) #2
    info.append(pAgua) #1
    info.append(pTierra) #1
    info.append(pCesped) #1
    info.append(pSuperficieEsperada) #3

    return info

def penalizarLineasArena(cuadricula, width, height):
    umbral = max(5, int(min(width, height) * 0.2))  # 8% del tamaño mínimo, mínimo 5
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
    penalizacion = min(20,penalizacion)


    return penalizacion,longitud_total,total_lineas,umbral

def verificarBordes(cuadricula, width, height, bordes, extension):
    contador_borde = 0
    contador_costa_interna = 0

    # Contar casillas no-mar en los bordes
    for (x, y) in bordes:
        if cuadricula[x][y][0] != 'mar':
            contador_borde += 1

    # Buscar casillas de costa interna
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if cuadricula[y][x][0] == 'mar':
                continue
            # Verificar si tiene mar como vecino (costa)
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = y + dy, x + dx
                if cuadricula[ny][nx][0] == 'mar':
                    contador_costa_interna += 1
                    break  # Solo contar una vez


    porcentaje  = contador_borde/(contador_borde+contador_costa_interna)
    print("Contador borde:", contador_borde)
    print("Contador costa interna:", contador_costa_interna)
    print("Porcentaje borde sobre costa:", porcentaje*100)

    return porcentaje*100

def funcionCalidad(tiempo, superBordes, arenaConectada, pAgua, pTierra, pCesped, pSuperEsperada,penalizacionLineas,longitud_actual,totalLineas,umbral):
    # Penalización extrema si demasiada isla toca el borde
    if superBordes < 15:
        print(f"❌ Penalización máxima: demasiada tierra fuera del borde ({superBordes}%). Puntuación = 0")
        return 0

    # Penalización progresiva por no tocar bordes (hasta 15 puntos de penalización)
    if(15 < superBordes < 30):
        penalizacionBordes = 0
    elif( 30 < superBordes < 65):
        penalizacionBordes = 7
    else:
        penalizacionBordes = 15
    print(f"🚧 Penalización por isla fuera de los bordes ({superBordes}% de la isla): -{penalizacionBordes} puntos")

    # Penalización por diferencia entre tierra y césped
    diferenciaTierraCesped = abs(pTierra- pCesped*1.5)
    penalizacionTierraCesped = round(min(diferenciaTierraCesped * 0.5, 20), 2)  # Máx. 15 puntos
    print(f"🌱 Penalización por diferencia tierra/césped ({pTierra}% vs {pCesped*1.5}%): -{penalizacionTierraCesped} puntos")

    # Penalización por tierra conectada del mar
    penalizacionArena = round(max(0, 100 - arenaConectada) * 0.5, 2)  # Máx. 30 puntos
    print(f"🏝️ Penalización por arena no conectada al mar ({arenaConectada}% conectada): -{penalizacionArena} puntos")


    #Penalizacion por islas irregulares
    print(f"📐 Penalización por líneas rectas de arena:")
    print(f"    ➤ Longitud minima: {umbral}")
    print(f"    ➤ Líneas encontradas: {totalLineas}")
    print(f"    ➤ Longitud total de líneas: {longitud_actual}")
    print(f"    ➤ Penalización aplicada: -{penalizacionLineas} puntos")


    # Penalización por desviación de la superficie esperada
    penalizacionSuperficie = round((100 - pSuperEsperada)*0.6, 2)  # Máx. 15 puntos
    print(f"📏 Penalización por diferencia en superficie esperada ({pSuperEsperada}% logrado): -{penalizacionSuperficie} puntos")

    # Penalización por tiempo de ejecución
    penalizacionTiempo = round(min(tiempo * 10, 20), 2)  # Penaliza 2 puntos por segundo, hasta un máximo de 20 puntos
    print(f"⏳ Penalización por tiempo de ejecución ({tiempo:.2f}s): -{penalizacionTiempo} puntos")

    # Cálculo de la puntuación final
    puntuacion = 100 - (penalizacionBordes + penalizacionTierraCesped + penalizacionArena + penalizacionLineas + penalizacionSuperficie + penalizacionTiempo)

    # No permitir puntuaciones negativas
    puntuacion = max(0, round(puntuacion, 2))
    print(f"✅ Puntuación final: {puntuacion} puntos")

    return puntuacion


############ INICIALIZACIÓN ###########
bordes = obtenerBordes(width,height)
extensionCosta = random.randint(1,5)
print(extensionCosta/10)
areaCosta = int((height * width) * extensionCosta/10)
areaAgua = 0.9  # Máximo porcentaje de agua permitido
limiteAgua = [areaCosta * areaAgua, 0]

inicializarCosta(cuadricula, height, width, limiteAgua, markov, tiles)
contFinal = 0

for _ in range(areaCosta):
    casillaElegida = seleccionarCasilla(cuadricula, height, width)
    if casillaElegida is None:
        break
    colapsarCasilla(cuadricula, casillaElegida, limiteAgua)
    propagarCasilla(cuadricula, casillaElegida, width, height, markov, tiles)
#skinMar(cuadricula,width,height,areaCosta)


###### CALIDAD ########

#### EXTRAS ####

fin = time.time()
tiempoEjec = fin - inicio
print("Tiempo de ejecucion:",round(tiempoEjec,4),end="s\n")


superBordes = verificarBordes(cuadricula,width,height,bordes,extensionCosta/10)
tierraAlMar = verificarArena(cuadricula,width,height)
infoBiomas = contrastarBiomas(cuadricula,width,height,extensionCosta/10)

pMar = infoBiomas[0]
pAgua = infoBiomas[1]
pTierra = infoBiomas[2]
pCesped = infoBiomas[3]
pSuperEsperada = infoBiomas[4]

puntuacionLineas,longitud_actual,totalLineas,umbral= penalizarLineasArena(cuadricula, width, height)
puntuacion = funcionCalidad(tiempoEjec,superBordes,tierraAlMar,pAgua,pTierra,pCesped,pSuperEsperada,puntuacionLineas,longitud_actual,totalLineas,umbral)

####### VISUALIZACIÓN ##########
colores = {'arena': (194, 178, 128), 'agua': (64, 164, 223), 'tierra': (139, 69, 19), 'cesped': (45, 87, 44), 'tierra2': (100, 50, 20), 'cesped2': (25, 60, 25), 'mar': (50, 0, 223), 'marProfundo': (0,0,120)}

imagen = np.zeros((height, width, 3), dtype=np.uint8)
for i in range(height):
    for j in range(width):
        tile = cuadricula[i][j][0]
        if tile in colores:
            imagen[i, j] = colores[tile]

plt.imshow(imagen)
plt.title(f"Costa generada por Colapso de Onda")
plt.axis('on')
plt.show()
