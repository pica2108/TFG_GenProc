import numpy as np
import matplotlib.pyplot as plt
import random

def generar_plano(frecuencia):
    tamaño = 10
    fig, ax = plt.subplots(figsize=(8, 8))
    celdas = np.linspace(0, tamaño, frecuencia + 1)

    # Almacenar los centros en una matriz
    centros = []

    for i in range(frecuencia):
        fila_centros = []
        for j in range(frecuencia):
            x0, y0 = celdas[i], celdas[j]
            ancho = celdas[i+1] - x0
            alto = celdas[j+1] - y0

            # Color gris aleatorio
            gris = random.random()
            ax.add_patch(plt.Rectangle((x0, y0), ancho, alto, color=(gris, gris, gris)))

            # Centro de la celda
            centro_x = x0 + ancho / 2
            centro_y = y0 + alto / 2

            # Dibujar punto azul claro
            ax.plot(centro_x, centro_y, 'o', color='#66b3ff', markersize=4)
            fila_centros.append((centro_x, centro_y))
        centros.append(fila_centros)

    # Unir puntos vecinos formando cuadrados y etiquetar esquinas
    for i in range(frecuencia - 1):
        for j in range(frecuencia - 1):
            # Obtener puntos en orden P1 a P4
            P1 = centros[i][j+1]     # arriba izquierda
            P2 = centros[i+1][j+1]   # arriba derecha
            P3 = centros[i+1][j]     # abajo derecha
            P4 = centros[i][j]       # abajo izquierda

            cuadrado = [P1, P2, P3, P4, P1]
            xs, ys = zip(*cuadrado)
            ax.plot(xs, ys, color='#66b3ff', linewidth=1)

            # Etiquetas
            offset = 0.2  # pequeño desplazamiento para que no se sobreponga al punto
            ax.text(P1[0] + offset, P1[1] + offset, "P1", fontsize=8, color='white')
            ax.text(P2[0] + offset, P2[1] + offset, "P2", fontsize=8, color='white')
            ax.text(P3[0] + offset, P3[1] - offset, "P3", fontsize=8, color='white')
            ax.text(P4[0] - offset, P4[1] - offset, "P4", fontsize=8, color='white')

    # Dibujar líneas de la cuadrícula
    for x in celdas:
        ax.axvline(x, color='black', lw=0.5)
        ax.axhline(x, color='black', lw=0.5)

    ax.set_aspect('equal', 'box')
    plt.axis('off')
    plt.show()

# Pedir frecuencia al usuario
frecuencia = 2
generar_plano(frecuencia)
