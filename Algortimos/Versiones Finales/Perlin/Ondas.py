import numpy as np
import matplotlib.pyplot as plt

# Solicitar al usuario la frecuencia y la amplitud
frecuencia = 2
amplitud = 0.5

# Parámetros de la onda
duracion = 1.0  # segundos
muestras_por_segundo = 1000
t = np.linspace(0, duracion, int(muestras_por_segundo * duracion), endpoint=False)

# Crear la onda senoidal
onda = amplitud * np.sin(2 * np.pi * frecuencia * t)

# Graficar la onda
plt.figure(figsize=(10, 4))
plt.plot(t, onda)
plt.title(f'Frecuencia: {frecuencia} , Amplitud: {amplitud}')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.ylim(-1, 1)  # Escala fija para ver bien la amplitud
plt.grid(True)
plt.tight_layout()
plt.show()
