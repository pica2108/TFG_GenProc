import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random


# Extraer patrones de la imagen
def extraer_patrones(imagen, tamano_tile):
    patrones = []
    alto, ancho = imagen.shape

    for i in range(alto - tamano_tile + 1):
        for j in range(ancho - tamano_tile + 1):
            tile = imagen[i:i + tamano_tile, j:j + tamano_tile]
            patrones.append(tile)

    # Convertir patrones a formas hashables
    patrones_unicos = {tuple(tile.flatten()) for tile in patrones}
    return [np.array(pattern).reshape(tamano_tile, tamano_tile) for pattern in patrones_unicos]


# Analizar vecindad entre patrones
def analizar_vecindad(patrones, tamano_tile):
    reglas = {tuple(pattern.flatten()): {'arriba': [], 'abajo': [], 'izquierda': [], 'derecha': []} for pattern in
              patrones}

    for pattern_a in patrones:
        for pattern_b in patrones:
            if np.array_equal(pattern_a[1:], pattern_b[:-1]):  # Arriba-abajo
                reglas[tuple(pattern_a.flatten())]['abajo'].append(tuple(pattern_b.flatten()))
            if np.array_equal(pattern_a[:-1], pattern_b[1:]):  # Abajo-arriba
                reglas[tuple(pattern_a.flatten())]['arriba'].append(tuple(pattern_b.flatten()))
            if np.array_equal(pattern_a[:, 1:], pattern_b[:, :-1]):  # Izquierda-derecha
                reglas[tuple(pattern_a.flatten())]['derecha'].append(tuple(pattern_b.flatten()))
            if np.array_equal(pattern_a[:, :-1], pattern_b[:, 1:]):  # Derecha-izquierda
                reglas[tuple(pattern_a.flatten())]['izquierda'].append(tuple(pattern_b.flatten()))

    return reglas


# Implementación del algoritmo Wave Function Collapse
def wave_function_collapse(ancho, alto, patrones, reglas):
    canvas = [[set([tuple(pattern.flatten()) for pattern in patrones]) for _ in range(ancho)] for _ in range(alto)]

    while True:
        opciones = [(i, j, canvas[i][j]) for i in range(alto) for j in range(ancho) if len(canvas[i][j]) > 1]
        if not opciones:
            break  # Terminar si todas las celdas están resueltas

        i, j, opciones_celda = random.choice(opciones)
        patron_seleccionado = random.choice(list(opciones_celda))
        canvas[i][j] = {patron_seleccionado}

        actualizar_vecinos(canvas, i, j, patron_seleccionado, reglas)

    return canvas


def actualizar_vecinos(canvas, i, j, patron, reglas):
    for di, dj, direccion in [(-1, 0, 'arriba'), (1, 0, 'abajo'), (0, -1, 'izquierda'), (0, 1, 'derecha')]:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(canvas) and 0 <= nj < len(canvas[0]) and len(canvas[ni][nj]) > 1:
            opciones_compatibles = reglas[patron][direccion]
            canvas[ni][nj].intersection_update(opciones_compatibles)


# Reconstruir la imagen a partir del canvas
def reconstruir_imagen(canvas, tamano_tile):
    alto = len(canvas)
    ancho = len(canvas[0])
    imagen = np.zeros((alto * tamano_tile, ancho * tamano_tile), dtype=int)

    for i in range(alto):
        for j in range(ancho):
            patron = np.array(list(canvas[i][j])[0]).reshape(tamano_tile, tamano_tile)
            imagen[i * tamano_tile:(i + 1) * tamano_tile, j * tamano_tile:(j + 1) * tamano_tile] = patron

    return imagen


# Flujo principal
if __name__ == "__main__":
    # Cargar imagen de entrada y convertirla en binaria
    imagen = Image.open("image.png").convert("L")
    imagen = (np.array(imagen) > 128).astype(int)  # Convertir a blanco y negro

    # Parámetros
    tamano_tile = 3
    patrones = extraer_patrones(imagen, tamano_tile)
    reglas = analizar_vecindad(patrones, tamano_tile)

    # Generar nueva imagen
    ancho, alto = 10, 10  # Dimensiones deseadas
    canvas = wave_function_collapse(ancho, alto, patrones, reglas)
    imagen_generada = reconstruir_imagen(canvas, tamano_tile)

    # Mostrar la imagen generada
    plt.imshow(imagen_generada, cmap="gray")
    plt.show()
