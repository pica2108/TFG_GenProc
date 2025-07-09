import matplotlib.pyplot as plt

# Coordenadas de los puntos
x1, y1 = 1, 1
x2, y2 = 5, 4

# Valor x3 para interpolar
x3 = 3

# Interpolación lineal para encontrar y3
# y3 = y1 + (x3 - x1)*(y2 - y1)/(x2 - x1)
y3 = y1 + (x3 - x1) * (y2 - y1) / (x2 - x1)

# Dibujar los puntos
plt.plot([x1, x2], [y1, y2], 'k-', label='Línea entre P1 y P2')  # Línea P1-P2
plt.plot([x1, x3], [y1, y3], 'b--', label='Base del triángulo')  # Línea P1-P3
plt.plot([x3, x3], [y1, y3], 'g--', label='Altura del triángulo')  # Línea vertical

# Marcar los puntos
plt.scatter([x1, x2, x3], [y1, y2, y3], color='red')
plt.text(x1, y1 - 0.2, 'P1 (x1,y1)', ha='center')
plt.text(x2, y2 + 0.2, 'P2 (x2,y2)', ha='center')
plt.text(x3, y3 + 0.2, 'P3 (x3,y3)', ha='center')

# Ajustes del gráfico
plt.title('Ejemplo de Interpolación Lineal')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()
