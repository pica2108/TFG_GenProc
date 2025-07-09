import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Parámetros
filas = 100
columnas = 100
iteraciones_suavizado = 5

# Generar plano inicial aleatorio
plano = np.random.uniform(0, 1, (filas, columnas))

# Función para verificar si la posición es válida
def esPosicionValida(fila, columna, filas, columnas):
    return 0 <= fila < filas and 0 <= columna < columnas

# Función para obtener vecinos
def calcularVecinos(fila, columna, filas, columnas):
    direcciones = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),         (0, 1),
                   (1, -1), (1, 0), (1, 1)]
    vecinos = []
    for f, c in direcciones:
        filaNueva = fila + f
        columnaNueva = columna + c
        if esPosicionValida(filaNueva, columnaNueva, filas, columnas):
            vecinos.append((filaNueva, columnaNueva))
    return vecinos

# Suavizar el terreno para dar forma de islas
for _ in range(3):
    nuevo_plano = np.copy(plano)
    for fila in range(filas):
        for columna in range(columnas):
            vecinos = calcularVecinos(fila, columna, filas, columnas)
            mediaVecinos = sum(plano[x][y] for x, y in vecinos) / len(vecinos)
            nuevo_plano[fila][columna] = mediaVecinos
    plano = nuevo_plano

# Colormap personalizado (mar, arena, tierra, cesped)
colors = ["#f4e285", "#0044aa", "#3ba635", "#a87c4f"]
bounds = [0.4, 0.45, 0.5, 0.55, 0.6]
cmap = ListedColormap(colors)
norm = plt.Normalize(vmin=0, vmax=1)

# Dibujar mapa
plt.figure(figsize=(8, 8))
plt.imshow(plano, cmap=cmap, norm=norm)
plt.colorbar(label='Altura / Bioma')
plt.title("Mapa de Islas con Biomas")
plt.axis('off')
plt.show()
