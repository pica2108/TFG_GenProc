import numpy as np
import matplotlib.pyplot as plt
import perlin


# Generar ruido de Perlin
def generate_perlin_noise_2d(width, height, scale, seed):
    perlin_noise = perlin.Perlin(seed)
    noise_map = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            noise_map[i][j] = perlin_noise.two(j / scale, i / scale)  # Coordenadas escaladas

    return noise_map

# Parámetros de la imagen
width = 1000
height = 1000
scale = 1.0
seed = 677567
# Generar y visualizar el ruido
noise_map = generate_perlin_noise_2d(width, height, scale, seed)


plt.imshow(noise_map, cmap='gray')
plt.colorbar()
plt.title("Mapa de Ruido de Perlin")
plt.show()