import numpy as np
import matplotlib.pyplot as plt


# Definir las regiones
def obtenerRegion(x, y):
    suma = x + y
    if suma <= 5:  # Región blanca
        return "blanco"
    elif 5 < suma <= 10:  # Región gris
        return "gris"
    else:  # Región negra
        return "negro"


# Obtener una nueva casilla dentro de la región con cierta probabilidad
def obtenerCasilla(region):
    if region == "blanco":
        # Para blancos, usar valores entre 0 y 0.25
        return np.random.uniform(0, 0.25)
    elif region == "gris":
        # Para grises, usar valores entre 0.26 y 0.75
        return np.random.uniform(0.26, 0.75)
    else:
        # Para negros, usar valores entre 0.76 y 1
        return np.random.uniform(0.76, 1)


# Generamos una matriz 10x10 con valores aleatorios entre 0 y 1 (ruido blanco)
ruido_blanco = np.random.uniform(0, 1, (10, 10))

# Nueva matriz suavizada para almacenar los resultados
ruido_blanco_suavizado = np.zeros((10, 10))

# Contadores de colores
contBlancos = 0
contGrises = 0
contNegros = 0

# Recorrer la matriz de ruido blanco original
for i, fila in enumerate(ruido_blanco):
    for j, casilla in enumerate(fila):
        # Obtener la región de la casilla actual
        region = obtenerRegion(i, j)

        # Asignar un nuevo valor a la casilla suavizada según la región
        if region == "blanco":
            ruido_blanco_suavizado[i][j] = obtenerCasilla("blanco")
            contBlancos += 1
        elif region == "gris":
            ruido_blanco_suavizado[i][j] = obtenerCasilla("gris")
            contGrises += 1
        else:
            ruido_blanco_suavizado[i][j] = obtenerCasilla("negro")
            contNegros += 1

# Visualizar el ruido blanco original
plt.imshow(ruido_blanco, cmap='gray_r')
plt.colorbar()
plt.title("Ruido Blanco Original")
plt.show()

# Visualizar el ruido suavizado
plt.imshow(ruido_blanco_suavizado, cmap='gray_r')
plt.colorbar()
plt.title("Ruido Blanco Suavizado")
plt.show()

# Imprimir los contadores
print("Blancos:", contBlancos)
print("Grises:", contGrises)
print("Negros:", contNegros)
