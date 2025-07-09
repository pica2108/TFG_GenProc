import numpy as np
import matplotlib.pyplot as plt
import perlin


# Generar el perfil del terreno con ruido de Perlin y simplificarlo para plataformas
def generate_platforms(width, scale, seed, threshold):
    perlin_noise = perlin.Perlin(seed)
    height_map = np.zeros(width)

    for x in range(width):
        # Generar valor de ruido de Perlin para cada columna 'x'
        noise_value = perlin_noise.one(x / scale)

        # Normalizar el valor del ruido entre [0, 1] para convertirlo en una altura
        normalized_value = (noise_value + 1) / 2  # Normalizar a [0, 1]

        # Multiplicar por la altura máxima del juego (por ejemplo, 30 bloques de altura)
        max_height = 30
        height = int(normalized_value * max_height)

        # Simplificar el valor de altura para formar plataformas planas
        if height % threshold == 0:
            height_map[x] = height
        else:
            height_map[x] = (height // threshold) * threshold  # Agrupar alturas para hacerlas planas

    return height_map


# Visualizar las plataformas en 2D
def visualize_platforms(height_map):
    width = len(height_map)
    max_height = int(np.max(height_map))

    # Crear un mapa binario de 0s y 1s para representar las plataformas
    platform_map = np.zeros((max_height + 1, width))

    # Llenar el mapa con plataformas
    for x in range(width):
        platform_height = int(height_map[x])
        platform_map[platform_height:, x] = 1  # Marcar como plataformas desde la altura hacia abajo

    # Visualizar el mapa
    plt.imshow(platform_map, cmap='gray', origin='lower')
    plt.title("Mapa de plataformas generadas con ruido de Perlin")
    plt.show()


# Parámetros
width = 200  # Ancho del mapa (ejemplo: 200 bloques)
scale = 1.0  # Escala del ruido de Perlin
seed = 6789  # Semilla para generar el ruido de Perlin
threshold = 0.1  # Umbral para la simplificación de alturas (agrupa alturas cada 'threshold' bloques)

# Generar el perfil de terreno simplificado para plataformas
height_map = generate_platforms(width, scale, seed, threshold)

# Visualizar las plataformas
visualize_platforms(height_map)
