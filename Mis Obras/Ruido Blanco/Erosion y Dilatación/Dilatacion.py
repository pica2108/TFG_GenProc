import numpy as np
import matplotlib.pyplot as plt
import cv2


def dilatar(ruidoBlanco,umbral,kernelDim,iteraciones):
    #(Si el valor es 0.5 o menos será un color y si no otro)
    ruido_binario = (ruidoBlanco > umbral).astype(np.uint8) * 255  # Escalamos a 0 y 255


    kernel = np.ones((kernelDim, kernelDim), np.uint8)


    erosion = cv2.dilate(ruido_binario, kernel, iterations=iteraciones)

    return ruido_binario,erosion



ruido_blanco = np.random.uniform(0, 1, (100, 100))

ruido_binario,dilatacion= dilatar(ruido_blanco,0.8,2,1)



plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.title("Original (Ruido Blanco)")
plt.imshow(ruido_blanco, cmap='gray_r')
plt.colorbar()

plt.subplot(1, 3, 2)
plt.title("Binario")
plt.imshow(ruido_binario, cmap='gray')
plt.colorbar()

plt.subplot(1, 3, 3)
plt.title("Erosión (3 iteraciones)")
plt.imshow(dilatacion, cmap='gray')
plt.colorbar()

plt.tight_layout()
plt.show()
