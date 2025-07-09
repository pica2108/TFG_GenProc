import random

import numpy as np
import matplotlib.pyplot as plt
import random
import perlin


semilla = random.randint(10000,10000000)
print(semilla)
perlin_noise = perlin.Perlin(semilla)


frecuencia = 3 #subdivisiones de la cuadricula
#la ampltud será el color de cada sector

'''noise_map = np.zeros((height, width))


for i in range(height):
    for j in range(width):
        noise_map[i][j] = perlin_noise.two(j / scale, i / scale)

print(perlin_noise)'''