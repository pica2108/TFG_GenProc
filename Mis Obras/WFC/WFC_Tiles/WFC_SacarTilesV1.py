import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def obtenerDivisores(n):
    divisores = []
    for i in range(1, (int(n**0.5)) + 1):
        if n % i == 0:
            divisores.append(i)
            if i != n // i:  # Añadir el divisor complementario
                divisores.append(n // i)
    divisores.sort()  # Ordenar los divisores
    return divisores
def reducirTiles(ladoTileX,ladoTileY,cuadradosTotales,alto,ancho):
    cont = -1
    while(cuadradosTotales % 1 == 0) and ladoTileX <= ancho and ladoTileY <= alto:
        nuevosDivisores = obtenerDivisores(cuadradosTotales)
        divisorMinimo = nuevosDivisores[1]
        cuadradosTotales = cuadradosTotales / divisorMinimo
        ladoTileX = ladoTileX * divisorMinimo
        ladoTileY = ladoTileY * divisorMinimo
        cont += 1

    cuadradosTotales = cuadradosTotales * divisorMinimo
    ladoTileX = ladoTileX / divisorMinimo
    ladoTileY = ladoTileY / divisorMinimo

    return int(cuadradosTotales), int(ladoTileX), int(ladoTileY)



imagen = Image.open(r'/imagenesWFC/pruebaTilesDefinidos/prueba.png')
imagenRGB = imagen.convert('RGB')
imagenPixeles = np.array(imagenRGB)

alto, ancho, _= imagenPixeles.shape
divisoresX = obtenerDivisores(ancho)
divisoresY = obtenerDivisores(alto)
print(divisoresY,divisoresX)
divisorX = divisoresX[len(divisoresX)-2]
divisorY = divisoresY[len(divisoresY)-2]

numTilesX = divisorX
numTilesY = divisorY
cuadradosTotales = numTilesX + numTilesY

ladoTileX = int(ancho / divisorX)
ladoTileY = int(alto / divisorY)

print(f"Dimensiones de la imagen: {ancho}x{alto}")

cuadradosTotalesFinales, ladoTileXFinal, ladoTileYFinal = reducirTiles(ladoTileX,ladoTileY,cuadradosTotales,alto,ancho)
print(f"Tamaño de cada cuadrado: {ladoTileX} x {ladoTileY}")
print("Cuadrados totales:", cuadradosTotales)



# Extraer los tiles
tiles = []
for x in range(0, ancho - ladoTileXFinal + 1, ladoTileXFinal):
    for y in range(0, alto - ladoTileYFinal + 1, ladoTileYFinal):
        tile = imagenPixeles[y:y + ladoTileYFinal, x:x + ladoTileXFinal]  # Extraemos el tile de tamaño definido
        tiles.append(tile)

# Mostrar los tiles extraídos
num_tiles = len(tiles)
num_cols = 10  # Cuántos tiles por fila queremos mostrar

fig, axes = plt.subplots(nrows=(num_tiles // num_cols) + 1, ncols=num_cols, figsize=(15, 10))
axes = axes.flatten()

for i, tile in enumerate(tiles):
    axes[i].imshow(tile)
    axes[i].axis('off')  # Ocultar los ejes de cada tile

# Si hay menos tiles que espacios, ocultar los ejes vacíos
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

print(len(tiles))
plt.tight_layout()
plt.show()
