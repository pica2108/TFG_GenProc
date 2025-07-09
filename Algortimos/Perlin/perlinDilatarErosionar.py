import random
import sys

import cv2
from perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt


def dilatarYErosionar(ruidoBlanco,umbral,kernelDim,iteraciones):

    ruido_binario = (ruidoBlanco > umbral).astype(np.uint8) * 255

    kernel = np.ones((kernelDim, kernelDim), np.uint8)  # Kernel 3x3

    dilatacion = cv2.dilate(ruido_binario, kernel, iterations=iteraciones)
    erosion =  cv2.erode(ruido_binario, kernel, iterations=iteraciones)

    return ruido_binario,dilatacion,erosion

def generar_ruido_perlin(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial,persistencia,persistencia2):
    ruido = np.zeros((filas, columnas))
    noise = PerlinNoise(seed=semilla)

    for octava in range(octavas):
        frecuencia = frecuencia_inicial * (persistencia ** octava)
        amplitud = amplitud_inicial / (persistencia2 ** octava)

        for i in range(filas):
            for j in range(columnas):
                ruido[i, j] += noise([i / filas * frecuencia, j / columnas * frecuencia]) * amplitud

    return ruido


filas, columnas = 100, 100 #Determinan el lienzo, no las divisiones
frecuencia_inicial = 3
'''
Subdivisiones de la primera octava (1 = 1 corte horizontal y otro vertical)
Imaginaldo como una onda, a mas frecuencia mas variacion de colores en un espacio determinado, menos frecuencia 
da pie a cambios mas suaves y extendidos
'''
octavas = 4
semilla = random.randint(1,100000)
amplitud_inicial = 10
persistencia = 6
pers2 = 6
# Generar el ruido
ruido_perlin = generar_ruido_perlin(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial,persistencia,pers2)



umbral = 0.5
kernelDim = 3
iteraciones = 2
binario, dilatacion, erosion = dilatarYErosionar(ruido_perlin,umbral,kernelDim,iteraciones)


fig, axes = plt.subplots(1, 4, figsize=(15, 6))

axes[0].imshow(ruido_perlin, cmap='gray')
axes[0].set_title(f"Ruido Perlin #{semilla}")
axes[0].axis('off')


axes[1].imshow(binario, cmap='gray')
axes[1].set_title(f"Binario")
axes[1].axis('off')


axes[2].imshow(dilatacion, cmap='gray')
axes[2].set_title(f"Dilatación")
axes[2].axis('off')


axes[3].imshow(erosion, cmap='gray')
axes[3].set_title(f"Erosion")
axes[3].axis('off')


plt.tight_layout()
plt.show()


