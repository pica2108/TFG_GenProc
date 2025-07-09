import numpy as np
import matplotlib.pyplot as plt
import perlin

# Función para mapear valores de ruido a colores personalizados
def map_color(value):
    if value < -0.1:
        return [0, 0, 0.5]  # Agua profunda (azul oscuro)
    elif value < 0.0:
        return [0, 0, 1]    # Agua superficial (azul claro)
    elif value < 0.1:
        return [0.8, 0.7, 0.5]  # Arena (beige)
    elif value < 0.3:
        return [0.1, 0.5, 0.1]  # Pasto (verde)
    elif value < 0.5:
        return [0.4, 0.4, 0.2]  # Colinas (verde oscuro)
    else:
        return [0.5, 0.5, 0.5]  # Montaña (gris)

# Generar ruido de Perlin con múltiples octavas
def generate_perlin_noise_2d(width, height, scale, seed, octaves):
    perlin_noise = perlin.Perlin(seed)
    noise_map = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            amplitude = 1
            frequency = 1
            total = 0

            for octave in range(octaves):
                sample_x = j / scale * frequency
                sample_y = i / scale * frequency
                total += perlin_noise.two(sample_x, sample_y) * amplitude

                amplitude *= 0.5
                frequency *= 2

            noise_map[i][j] = total

    # Normalizar el ruido para que esté entre -1 y 1
    max_value = np.max(noise_map)
    min_value = np.min(noise_map)
    normalized_noise_map = (noise_map - min_value) / (max_value - min_value) * 2 - 1  # Escala a [-1, 1]

    return normalized_noise_map

# Parámetros de la imagen
width = 500
height = 500
scale = 1.0
seed = 6789
octaves = 1

# Generar ruido
noise_map = generate_perlin_noise_2d(width, height, scale, seed, octaves)

# Mapa de colores basado en los valores de ruido
colored_map = np.zeros((height, width, 3))  # Mapa con 3 canales (RGB)

# Asignar colores basados en el valor de ruido
for i in range(height):
    for j in range(width):
        colored_map[i][j] = map_color(noise_map[i][j])

# Visualizar el mapa de colores
plt.imshow(colored_map)
plt.title("Mapa de Ruido de Perlin con Colores Personalizados")
plt.show()
