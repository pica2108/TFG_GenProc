import random
import sys

from perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt

def generar_ruido_perlin(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial,persistencia,persistencia2):
    ruido = np.zeros((filas, columnas))
    noise = PerlinNoise(seed=semilla)

    for octava in range(octavas):
        frecuencia = frecuencia_inicial * 2  # Duplica la frecuencia por octava
        amplitud = amplitud_inicial / 2      # Reduce la amplitud por octava

        for i in range(filas):
            for j in range(columnas):
                ruido[i, j] += noise([i / filas * frecuencia, j / columnas * frecuencia]) * amplitud

    return ruido

'''La funcion Noise coge los valores de i y j, que se han dividio por las filas y columnas para escalarlos al lienzo y se
le aplica la frecuencia y la amplitud, perlin sabe. Ese valor de perlin se coloca en la matriz de ruido'''


# Parámetros
filas, columnas = 200, 200 #Determinan el lienzo, no las divisiones
frecuencia_inicial = 2
'''
Subdivisiones de la primera octava (1 = 1 corte horizontal y otro vertical)
Imaginaldo como una onda, a mas frecuencia mas variacion de colores en un espacio determinado, menos frecuencia 
da pie a cambios mas suaves y extendidos
'''
octavas = 5 #Capas de ruido que se sumaran al final
semilla = random.randint(1,100000)
amplitud_inicial = 2
persistencia = 1 #Determina la variacion de la frecuencia y la amplitud en cada octava, 2 será duplicar la frecuencia y partir la amplitud
persistencia2 = 1

# Generar el ruido
ruido_perlin = generar_ruido_perlin(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial,persistencia,persistencia2)

# Visualizar
# Visualizar
plt.imshow(ruido_perlin, cmap='gray')
plt.title(f"#{semilla}")
plt.show()


