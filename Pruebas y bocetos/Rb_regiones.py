import numpy as np
import matplotlib.pyplot as plt



def obtenerRegion(x, y):
    suma = x + y
    if suma <= 5:
        return "blanco"
    elif 5 < suma <= 10:
        return "gris"
    else:
        return "negro"



def obtenerCasilla(region):
    if region == "blanco":

        return np.random.uniform(0, 0.25)
    elif region == "gris":

        return np.random.uniform(0.26, 0.75)
    else:

        return np.random.uniform(0.76, 1)



ruido_blanco = np.random.uniform(0, 1, (10, 10))


ruido_blanco_suavizado = np.zeros((10, 10))


contBlancos = 0
contGrises = 0
contNegros = 0

for i, fila in enumerate(ruido_blanco):
    for j, casilla in enumerate(fila):
        # Obtener la región de la casilla actual
        region = obtenerRegion(i, j)

        if region == "blanco":
            ruido_blanco_suavizado[i][j] = obtenerCasilla("blanco")
            contBlancos += 1
        elif region == "gris":
            ruido_blanco_suavizado[i][j] = obtenerCasilla("gris")
            contGrises += 1
        else:
            ruido_blanco_suavizado[i][j] = obtenerCasilla("negro")
            contNegros += 1


plt.imshow(ruido_blanco, cmap='gray_r')
plt.colorbar()
plt.title("Ruido Blanco Original")
plt.show()


plt.imshow(ruido_blanco_suavizado, cmap='gray_r')
plt.colorbar()
plt.title("Ruido Blanco Suavizado")
plt.show()


print("Blancos:", contBlancos)
print("Grises:", contGrises)
print("Negros:", contNegros)
