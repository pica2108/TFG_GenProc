import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = Image.open(r'C:\Users\gpica\Ciberseguridad\6º Curso\TFG\Proyectos\imagenesWFC\corales.png')
imagen_rgb = imagen.convert('RGB')

# Convertir la imagen a matriz de píxeles
pixeles = np.array(imagen_rgb)

# Definir tamaño de los "tiles" (por ejemplo, 3x3 píxeles)
tile_size = 30  # Cambia esto según el tamaño de tile que desees
ancho, alto = imagen.size

# Extraer los "tiles" de la imagen
tiles = []
for x in range(0, ancho - tile_size + 1, tile_size):
    for y in range(0, alto - tile_size + 1, tile_size):
        tile = pixeles[y:y + tile_size, x:x + tile_size]  # Extraemos el tile de tamaño tile_size
        tiles.append(tile)

# Mostrar los tiles extraídos
num_tiles = len(tiles)
num_cols = 10  # Cuántos tiles por fila queremos mostrar

fig, axes = plt.subplots(nrows=(num_tiles // num_cols) + 1, ncols=num_cols, figsize=(15, 10))
axes = axes.flatten()

for i, tile in enumerate(tiles):
    axes[i].imshow(tile)
    axes[i].axis('off')  # Ocultar los ejes de cada tile

plt.show()
