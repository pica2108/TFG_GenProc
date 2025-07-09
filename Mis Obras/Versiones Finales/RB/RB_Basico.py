import numpy as np
import matplotlib.pyplot as plt


#Generamos una matriz 100x100 con valores aleatorios entre -1 y 1
ruido_blanco = np.random.uniform(0, 1, (100, 100))
print(ruido_blanco)
plt.imshow(ruido_blanco, cmap='gray')
plt.colorbar()
plt.show()

'''# 0 - 0.25 Blancos
# 0.26 - 0.75 Grises
# 0.76 - 1 Negros'''

contBlancos = 0
contGrises = 0
contNegros = 0

for fila in ruido_blanco:
    for casilla in fila:
        if 0 <= casilla <0.25:
            contBlancos+=1
        elif 0.26 <= casilla <=0.75:
            contGrises+=1
        else:
            contNegros +=1
print(contBlancos,contGrises,contNegros)


'''Color Map Options:
'gray' 
'viridis'
'plasma'
'inferno'
'jet'
'coolwarm'

sufijo _r invierte el mapa de colores (jet_r)
'''