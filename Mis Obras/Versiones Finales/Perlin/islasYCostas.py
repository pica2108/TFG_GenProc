import random
import sys
import time

from perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt

inicio = time.time()

def generar_ruido_perlin(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial, persistencia, persistencia2):
    ruido = np.zeros((filas, columnas))
    noise = PerlinNoise(seed=semilla)

    for octava in range(octavas):
        frecuencia = frecuencia_inicial * (persistencia ** octava)
        amplitud = amplitud_inicial / (persistencia2 ** octava)

        for i in range(filas):
            for j in range(columnas):
                ruido[i, j] += noise([i / filas * frecuencia, j / columnas * frecuencia]) * amplitud

    return ruido


def map_color(value):
    if value < -0.5:
        return [0, 0, 0.5]  # Agua
    elif value < 0.0:
        return [0, 0, 1]    # Agua superficial (
    elif value < 0.5:
        return [0.8, 0.7, 0.5]  # Arena
    elif value < 1:
        return [0.1, 0.5, 0.1]  # Pasto
    elif value < 1.5:
        return [0.4, 0.4, 0.2]  # Colinas
    else:
        return [0.5, 0.5, 0.5]  # Montaña


####### Parámetros ######

filas, columnas = 150, 150
frecuencia_inicial = 4
octavas = 7
semilla = random.randint(1, 100000)
amplitud_inicial = 7
persistencia = 2
persistencia2 = persistencia


ruido_perlin = generar_ruido_perlin(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial, persistencia, persistencia2)
print(ruido_perlin)
mapa_coloreado = np.zeros((filas, columnas, 3))  # Mapa RGB

for i in range(filas):
    for j in range(columnas):
        valor = ruido_perlin[i, j]
        mapa_coloreado[i, j] = map_color(valor)

fin = time.time()

############## CALIDAD ###############



def map_tipo(value):
    if value < -0.5:
        return 'mar'
    elif value < 0.0:
        return 'mar'
    elif value < 0.5:
        return 'arena'
    elif value < 1:
        return 'cesped'
    elif value < 1.5:
        return 'colina'
    else:
        return 'montana'


def convertir_a_wfc(ruido_perlin):
    filas, columnas = ruido_perlin.shape
    cuadricula = []

    for i in range(filas):
        fila = []
        for j in range(columnas):
            tipo = map_tipo(ruido_perlin[i, j])
            fila.append((tipo, 1))  # Asumimos peso 1
        cuadricula.append(fila)

    return cuadricula


cuadricula_wfc = convertir_a_wfc(ruido_perlin)



def vecinos(x, y, width, height):
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [(y + dy, x + dx) for dx, dy in direcciones if 0 <= x + dx < width and 0 <= y + dy < height]

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


def obtenerBordes(width, height):
    bordes = []

    margen_y_superior = round(height * 0.09)
    margen_y_inferior = round(height * 0.05)
    margen_x_izquierda = round(width * 0.08)
    margen_x_derecha = round(width * 0.04)

    for y in range(height):
        for x in range(width):
            if y < margen_y_superior or y >= height - margen_y_inferior or x < margen_x_izquierda or x >= width - margen_x_derecha:
                bordes.append((y, x))

    return bordes

def verificarBordes(cuadricula, width, height,bordes):
    contador = 0
    area = width * height
    for (x,y) in bordes:
        if cuadricula[x][y][0] != 'mar':
            contador += 1
    aux = (contador/area)*100
    superBordes = round(aux,2)
    return superBordes #Maxima

def verificarBordesCosta(cuadricula, width, height, bordes):
    contador_borde = 0
    contador_costa_interna = 0


    for (x, y) in bordes:
        if cuadricula[x][y][0] != 'mar':
            contador_borde += 1


    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if cuadricula[y][x][0] == 'mar':
                continue
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = y + dy, x + dx
                if cuadricula[ny][nx][0] == 'mar':
                    contador_costa_interna += 1
                    break


    porcentaje  = contador_borde/(contador_borde+contador_costa_interna)
    print("Contador borde:", contador_borde)
    print("Contador costa interna:", contador_costa_interna)
    print("Porcentaje borde sobre costa:", porcentaje*100)

    return porcentaje*100

def contrastarBiomas(cuadricula, width, height):
    info = []
    mar = 0
    montana = 0
    cesped = 0
    colina = 0
    area = width * height
    for fila in range(height):
        for columna in range(width):
            if cuadricula[fila][columna][0] == 'mar':
                mar += 1
            elif cuadricula[fila][columna][0] == 'montana':
                montana += 1
            elif cuadricula[fila][columna][0] == 'cesped':
                cesped += 1
            elif cuadricula[fila][columna][0] == 'colina':
                colina += 1

    print("Mar = ", mar)
    pMar = (round(mar/area,2)*100)
    superficie  = area - mar
    pCesped = round((cesped/superficie)*100,2)
    pColina = round((colina/superficie)*100,2)
    pMontana = round((montana/superficie)*100,2)

    info.append(pMar) #2
    #info.append(pAgua) #1
    info.append(pColina) #1
    info.append(pMontana)  # 1
    info.append(pCesped) #1
    #info.append(pSuperficieEsperada) #3

    return info


def penalizarLineasArena(cuadricula, width, height):
    umbral = max(6, int(min(width, height) * 0.1))
    total_lineas = 0
    longitud_total = 0
    contArena = 0
    for x in range(height):
        longitud_actual = 0
        for y in range(width):
            if cuadricula[x][y][0] == 'arena':
                contArena += 1
                vecinosCasilla = vecinos(x, y, height, width)
                for (i, j) in vecinosCasilla:
                    if cuadricula[j][i][0] == 'mar':
                        longitud_actual += 1
                        break
            else:
                if longitud_actual >= umbral:
                    total_lineas += 1
                    longitud_total += longitud_actual
                longitud_actual = 0
        if longitud_actual >= umbral:
            total_lineas += 1
            longitud_total += longitud_actual

    for x in range(height):
        longitud_actual = 0
        for y in range(width):
            if cuadricula[x][y][0] == 'arena':
                #contArena += 1
                vecinosCasilla = vecinos(x, y, height, width)
                for (i, j) in vecinosCasilla:
                    if cuadricula[j][i][0] == 'mar':
                        longitud_actual += 1
                        break
            else:
                if longitud_actual >= umbral:
                    total_lineas += 1
                    longitud_total += longitud_actual
                longitud_actual = 0
        # Final de la columna
        if longitud_actual >= umbral:
            total_lineas += 1
            longitud_total += longitud_actual


    penalizacion = round((total_lineas * longitud_total) / (width * height),7)*2000
    penalizacion = min(10,penalizacion)
    print("Arena:",contArena)

    return penalizacion,longitud_total,total_lineas,umbral


def funcionCalidadIslas(tiempo, superBordes, arenaConectada, pColina, pMontana,pCesped,penalizacionLineas,longitud_actual,totalLineas,umbral,costa):
    if not costa:
        if superBordes > 15:
            print(f"❌ Penalización máxima: demasiada isla tocando el borde ({superBordes}%). Puntuación = 0")
            return 0
        else:
            penalizacionBordes = round(min(superBordes*1.5, 15), 2)
            print(f"🚧 Penalización por isla en los bordes ({superBordes}% de la isla): -{penalizacionBordes} puntos")


    else:
        if superBordes < 15:
            print(f"❌ Penalización máxima: demasiada tierra fuera del borde ({superBordes}%). Puntuación = 0")
            return 0
        else:
            if (15 < superBordes < 30):
                penalizacionBordes = 0
            elif (30 < superBordes < 65):
                penalizacionBordes = 5
            else:
                penalizacionBordes = 10
            print(
                f"🚧 Penalización por isla fuera de los bordes ({superBordes}% de la isla): -{penalizacionBordes} puntos")


    colinaYCesped = pColina + pCesped
    diferencia = abs(pMontana - colinaYCesped)
    penalizacionTierraCesped = round(min(diferencia * 0.5, 15), 2)
    print(f"🌱 Penalización por diferencia Colina y Cesped/Montana ({colinaYCesped}% vs {pMontana}%): -{penalizacionTierraCesped} puntos")

    penalizacionArena = round(max(0, 100 - arenaConectada) * 0.3, 2)  # Máx. 30 puntos
    print(f"🏝️ Penalización por arena no conectada al mar ({arenaConectada}% conectada): -{penalizacionArena} puntos")



    print(f"📐 Penalización por líneas rectas de arena:")
    print(f"    ➤ Longitud minima: {umbral}")
    print(f"    ➤ Líneas encontradas: {totalLineas}")
    print(f"    ➤ Longitud total de líneas: {longitud_actual}")
    print(f"    ➤ Penalización aplicada: -{penalizacionLineas} puntos")


    penalizacionTiempo = round(min(tiempo * 2, 20), 2)  # Penaliza 2 puntos por segundo, hasta un máximo de 20 puntos
    print(f"⏳ Penalización por tiempo de ejecución ({tiempo:.2f}s): -{penalizacionTiempo} puntos")


    puntuacion = 100 - (penalizacionBordes + penalizacionTierraCesped + penalizacionArena + penalizacionLineas + penalizacionTiempo)

    puntuacion = max(0, round(puntuacion, 2))
    print(f"✅ Puntuación final: {puntuacion} puntos")

    return puntuacion
#################################


tiempoEjec = fin - inicio
print("Tiempo de ejecucion:",round(tiempoEjec,4),end="s\n")
tierraAlMar = verificarArena(cuadricula_wfc,filas,columnas)
print(tierraAlMar)
infoBiomas = contrastarBiomas(cuadricula_wfc,filas,columnas)
print(infoBiomas)
pen,longitud,lineas,umbral = penalizarLineasArena(cuadricula_wfc,filas,columnas)
print(pen,longitud,lineas,umbral)

costa = 0
bordes = obtenerBordes(filas,columnas)

if costa:
    superBordes = verificarBordesCosta(cuadricula_wfc,filas,columnas,bordes)
else:
    superBordes = verificarBordes(cuadricula_wfc,filas,columnas,bordes)

pMar = infoBiomas[0]
pColina = infoBiomas[1]
pMontana = infoBiomas[2]
pCesped = infoBiomas[3]



funcionCalidadIslas(tiempoEjec,superBordes,tierraAlMar,pColina,pMontana,pCesped,pen,longitud,lineas,umbral,costa)


plt.imshow(mapa_coloreado)
plt.title(f"Mapa generado con Perlin. Semilla: #{semilla}")
plt.show()



