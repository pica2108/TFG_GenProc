import numpy as np
import matplotlib.pyplot as plt
import perlin


# Generar el perfil del terreno con ruido de Perlin y simplificarlo para plataformas
def generate_platforms(width, scale, seed, threshold):
    perlin_noise = perlin.Perlin(seed)
    height_map = np.zeros(width)

    for x in range(width):

        noise_value = perlin_noise.one(x / scale)

        normalized_value = (noise_value + 1) / 2  # Normalizar a [0, 1]

        max_height = 30
        height = int(normalized_value * max_height)

        if height % threshold == 0:
            height_map[x] = height
        else:
            height_map[x] = (height // threshold) * threshold

    return height_map


def visualize_platforms(height_map):
    width = len(height_map)
    max_height = int(np.max(height_map))


    platform_map = np.zeros((max_height + 1, width))


    for x in range(width):
        platform_height = int(height_map[x])
        platform_map[platform_height:, x] = 1  # Marcar como plataformas desde la altura hacia abajo


    plt.imshow(platform_map, cmap='gray', origin='lower')
    plt.title("Mapa de plataformas generadas con ruido de Perlin")
    plt.show()



width = 200
scale = 1.0
seed = 6789
threshold = 0.1


height_map = generate_platforms(width, scale, seed, threshold)

visualize_platforms(height_map)
