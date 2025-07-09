import numpy as np
from PIL import Image
import glob
import matplotlib.pyplot as plt
import math

ruta_carpeta = r'C:\Users\gpica\Ciberseguridad\6º Curso\TFG\Proyectos\imagenesWFC\pruebaTilesDefinidos\tiles'

imagenes = []

for ruta_imagen in glob.glob(f"{ruta_carpeta}/*.png"):
    imagen = Image.open(ruta_imagen)
    imagenRGB = imagen.convert('RGB')
    imagenPixeles = np.array(imagenRGB)
    #print(imagenPixeles.size)
    imagenes.append(imagenPixeles)

print(imagenes[0][0])
extremosImagenes = []
for imagen in imagenes:
    particion = []

    arriba = imagen[0]
    particion.append(arriba)
    abajo = imagen[-1]
    particion.append(abajo)

    izquierda = imagen[:, 0, :]
    particion.append(izquierda)
    derecha = imagen[:, -1, :]
    particion.append(derecha)
    extremosImagenes.append(particion)

print(extremosImagenes[0][2])

'''imagen0 = imagenes[0]
print(imagen0[:, 0, :])'''

# PLT
num_imagenes = len(imagenes)
num_columnas = math.ceil(math.sqrt(num_imagenes))
num_filas = math.ceil(num_imagenes / num_columnas)

# Crear la figura de matplotlib
fig, axs = plt.subplots(num_filas, num_columnas, figsize=(8, 8))

# Aplanar los ejes (en caso de que haya un solo subplot, lo convertimos en una lista)
axs = axs.flatten()

# Mostrar cada imagen en el subplot correspondiente
for i, imagen in enumerate(imagenes):
    axs[i].imshow(imagen)
    axs[i].axis('off')  # Ocultar los ejes de cada imagen

# Ocultar ejes extra en caso de que sobren subplots
for j in range(i + 1, num_filas * num_columnas):
    axs[j].axis('off')

plt.tight_layout()
plt.show()
