from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def acotarImagen(imagen,alto,ancho):
    # Calcular la nueva dimensión (el lado del cuadrado perfecto)
    nueva_dimension = max(alto, ancho)

    # Crear una nueva imagen cuadrada de fondo blanco
    imagen_cuadrada = Image.new('RGB', (nueva_dimension, nueva_dimension), (0, 0, 0))

    # Pegar la imagen original en el centro de la nueva imagen cuadrada
    imagen_cuadrada.paste(imagenRGB, ((nueva_dimension - ancho) // 2, (nueva_dimension - alto) // 2))

    # Convertir la imagen cuadrada a un array para mostrarla con matplotlib
    imagen_cuadrada_array = np.array(imagen_cuadrada)

    return imagen_cuadrada_array

def mostrarImagen(imagen):
    # Mostrar la imagen usando matplotlib
    plt.imshow(imagenFinal)
    plt.axis('off')  # Ocultar ejes
    plt.show()  # Mostrar la imagen

# Cargar la imagen
imagen = Image.open(r'/imagenesWFC/pruebaTilesDefinidos/Muestra.png')
imagenRGB = imagen.convert('RGB')
imagenPixeles = np.array(imagenRGB)

# Obtener dimensiones actuales
alto, ancho, _ = imagenPixeles.shape
imagenFinal = acotarImagen(imagenPixeles,alto,ancho)
mostrarImagen(imagenFinal)
dimensionFinal,_,_= imagenFinal.shape

print("Dimension final de la imagen:", dimensionFinal, "x", dimensionFinal)