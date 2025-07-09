import numpy as np
import matplotlib.pyplot as plt

# Solicitar frecuencia y amplitud base
frecuencia_base = 2
amplitud_base = 2

# Tiempo en el que se evaluará la suma (un solo ciclo base)
t = np.linspace(0, np.pi, 1000)

# Sumar las ondas
suma = np.zeros_like(t)
num_armonicos = 5  # Puedes ajustar esto para más o menos detalle

for i in range(num_armonicos):
    freq = frecuencia_base * (2 ** i)
    amp = amplitud_base / (2 ** i)
    suma += amp * np.sin(freq * t)

# Graficar
plt.figure(figsize=(10, 4))
plt.plot(t, suma, color='black')
plt.grid(True)
plt.title('Suma de ondas armónicas')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.tight_layout()
plt.show()
