import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = Image.open(
    r'/imagenesWFC/pruebaTilesDefinidos/Muestra.png')
imagenRGB = imagen.convert('RGB')
ancho, alto = imagenRGB.size
print("Dimensión de imagen: ", alto, 'x', ancho)

# Definir el número de segmentos
numTilesX = 3  # Número de segmentos en horizontal
numTilesY = 3  # Número de segmentos en vertical

# Calcular las dimensiones de cada tile
ladoTileX = ancho / numTilesX  # Ancho de cada tile
ladoTileY = alto / numTilesY  # Alto de cada tile
print("Dimensión del tile: ", ladoTileX, 'x', ladoTileY)

# Crear una lista para almacenar los tiles
tiles = []

# Recortar la imagen en tiles
for i in range(numTilesY):
    for j in range(numTilesX):
        # Calcular las coordenadas del rectángulo a recortar
        left = j * ladoTileX
        upper = i * ladoTileY
        right = left + ladoTileX
        lower = upper + ladoTileY

        # Recortar el tile y añadirlo a la lista
        tile = imagenRGB.crop((left, upper, right, lower))
        tiles.append(tile)

# Mostrar los tiles
fig, axs = plt.subplots(numTilesY, numTilesX, figsize=(12, 8))
for ax, tile in zip(axs.flatten(), tiles):
    ax.imshow(tile)
    ax.axis('off')  # No mostrar los ejes

plt.tight_layout()
plt.show()
