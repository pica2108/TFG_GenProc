import numpy as np
import matplotlib.pyplot as plt

# Generar una matriz 2D de ruido blanco (por ejemplo, 100x100)
ruido_blanco = np.random.uniform(-1, 1, (100, 100))

# Visualizar el ruido blanco
plt.imshow(ruido_blanco, cmap='gray')
#print(ruido_blanco[0])
#print(len(ruido_blanco))
plt.show()