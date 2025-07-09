from collections import Counter

from PIL import Image
import numpy as np

# Cargar la imagen
imagen = Image.open(r'C:\Users\gpica\Ciberseguridad\6º Curso\TFG\Proyectos\imagenesWFC\banderaDudosa.png')  # Especifica la ruta de tu imagen

# Convertir la imagen a formato RGB (para asegurarte de trabajar con colores RGB)
imagen_rgb = imagen.convert('RGB')

# Convertir la imagen a una matriz numpy
matriz_pixeles = np.array(imagen_rgb)
# Mostrar información de la imagen
ancho, alto = imagen.size

# Inicializar un contador para almacenar la frecuencia de cada color
contador_colores = Counter()

# Recorrer cada píxel de la imagen
for x in range(ancho):
    for y in range(alto):
        # Obtener el valor RGB del píxel en la posición (x, y)
        color = imagen_rgb.getpixel((x, y))
        # Contar cuántas veces aparece cada color
        contador_colores[color] += 1

# Mostrar los colores más comunes
colores_comunes = contador_colores.most_common(10)  # Cambia 10 por el número de colores que quieres ver
for color, count in colores_comunes:
    print(f"Color {color} aparece {count} veces")