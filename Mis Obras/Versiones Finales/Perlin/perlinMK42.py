import random

import numpy as np
from matplotlib import pyplot as plt
from perlin_noise import PerlinNoise


###### PERLIN INICIAL  #######
def generar_ruido_perlin_restringido(filas, columnas, octavas, semilla, frecuencia_inicial, amplitud_inicial,restricciones=None):
    ruido = np.zeros((filas, columnas))
    noise = PerlinNoise(seed=semilla)
    persistencia = 2
    for octava in range(octavas):
        frecuencia = frecuencia_inicial * (persistencia ** octava)  # Duplica la frecuencia por octava
        amplitud = amplitud_inicial / (persistencia ** octava)  # Reduce la amplitud por octava

        for i in range(filas):
            for j in range(columnas):
                valor = noise([i / filas * frecuencia, j / columnas * frecuencia]) * amplitud

                # Aplica restricciones (si están definidas)
                if restricciones:
                    for restriccion in restricciones:
                        valor = restriccion(valor, i, j, filas, columnas)

                ruido[i, j] += valor

    return ruido


########## RESTRICCIONES INICIALES ########


def islasCentrales(valor, i, j, filas, columnas):

    centroX, centroY = filas / 2, columnas / 2
    distancia = ((i - centroX) ** 2 + (j - centroY) ** 2) ** 0.5 #Pitagoras entre el punto y el centro del plano para calcular distancia
    maxDistancia = ((filas / 2) ** 2 + (columnas / 2) ** 2) ** 0.5 #Pitagoras entre el centro y una esquina para saber distancia maxima
    escala = (distancia / maxDistancia) - 1  # De aqui sale la variacion, si el punto queda en la esquina, la escala sale 0 y el valor se queda como esta
    return valor * escala



###### RESTRICCIONES FINALES ####

def refinarIslas():
    return 0


# Parámetros
filas, columnas = 200, 200
frecuencia_inicial =6
octavas = 5
semilla = random.randint(1,10000)

# Generar ruido con restricciones
restricciones = []
ruido_restringido = generar_ruido_perlin_restringido(
    filas, columnas, octavas, semilla, frecuencia_inicial, frecuencia_inicial, restricciones
)

########  VISUALIZACION #########


def map_color(value):
    if value < 2:
        return [0, 0, 0.5]  # Agua profunda (azul oscuro)
    elif value < 1.5:
        return [0, 0, 1]    # Agua superficial (azul claro)
    elif value < 1:
        return [0.8, 0.7, 0.5]  # Arena (beige)
    elif value < 0.5:
        return [0.1, 0.5, 0.1]  # Pasto (verde)
    elif value < 0:
        return [0.4, 0.4, 0.2]  # Colinas (verde oscuro)
    else:
        return [0.5, 0.5, 0.5]  # Montaña (gris)
# Crear el mapa coloreado aplicando la función `map_color` a cada valor de ruido
mapa_coloreado = np.zeros((filas, columnas, 3))  # Mapa RGB

for i in range(filas):
    for j in range(columnas):
        valor = ruido_restringido[i, j]
        mapa_coloreado[i, j] = map_color(valor)

# Visualizar el resultado

'''plt.imshow(mapa_coloreado)
plt.title(f"Mapa de Islas con Semilla #{semilla}")
plt.axis('off')  # Desactivar los ejes para una vista más limpia
plt.show()

'''
plt.imshow(ruido_restringido, cmap='gray')

plt.show()


