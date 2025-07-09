import random

import numpy as np
from perlin_noise import PerlinNoise


def generar_ruido_perlin_restringido(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial,
                                     persistencia, persistencia2, restricciones=None):
    ruido = np.zeros((filas, columnas))
    noise = PerlinNoise(seed=semilla)

    for octava in range(octavas):
        frecuencia = frecuencia_inicial * (persistencia ** octava)  # Duplica la frecuencia por octava
        amplitud = amplitud_inicial / (persistencia2 ** octava)  # Reduce la amplitud por octava

        for i in range(filas):
            for j in range(columnas):
                valor = noise([i / filas * frecuencia, j / columnas * frecuencia]) * amplitud

                # Aplica restricciones (si están definidas)
                if restricciones:
                    for restriccion in restricciones:
                        valor = restriccion(valor, i, j, filas, columnas)

                ruido[i, j] += valor

    return ruido

#ISLAS CENTRALES
def islasCentrales(valor, i, j, filas, columnas):

    centroX, centroY = filas / 2, columnas / 2
    distancia = ((i - centroX) ** 2 + (j - centroY) ** 2) ** 0.5 #Pitagoras entre el punto y el centro del plano para calcular distancia
    maxDistancia = ((filas / 2) ** 2 + (columnas / 2) ** 2) ** 0.5 #Pitagoras entre el centro y una esquina para saber distancia maxima
    escala = (distancia / maxDistancia) -1  # De aqui sale la variacion, si el punto queda en la esquina, la escala sale 0 y el valor se queda como esta
    return valor * escala

#Si se cambia el 1 de escala se cambia el color
def venom(valor, i, j, filas, columnas):

    centroX, centroY = filas / 2, columnas / 2
    distancia = ((i - centroX) ** 2 + (j - centroY) ** 2) ** 0.5 #Pitagoras entre el punto y el centro del plano para calcular distancia
    maxDistancia = ((filas / 2) ** 2 + (columnas / 2) ** 2) ** 0.5 #Pitagoras entre el centro y una esquina para saber distancia maxima
    escala = (distancia/maxDistancia)    # De aqui sale la variacion, si el punto queda en la esquina, la escala sale 0 y el valor se queda como esta
    if valor < 0:
        return valor * escala * - 1
    else:
        return valor * escala

def rioHorizontal(valor, i, j, filas, columnas):
    anchoRio = filas * 0.1
    distanciaAlCentro = abs(i - filas / 2)
    escala = max(0, 1 - (distanciaAlCentro / anchoRio))
    return valor * (abs(1 - escala))


# Parámetros
filas, columnas = 150, 150
frecuencia_inicial =2
octavas = 5
semilla = random.randint(1,10000)
amplitud_inicial = 10
persistencia = 2
persistencia2 = 2


restricciones = [islasCentrales]
ruido_restringido = generar_ruido_perlin_restringido(
    filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial, persistencia, persistencia2, restricciones
)


import matplotlib.pyplot as plt

plt.imshow(ruido_restringido, cmap='gray')
#plt.colorbar()
plt.title("Ruido Perlin con Restricciones")
plt.show()
