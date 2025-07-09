import matplotlib.pyplot as plt

x1, y1 = 1, 1
x2, y2 = 5, 4


x3 = 3



y3 = y1 + (x3 - x1) * (y2 - y1) / (x2 - x1)


plt.plot([x1, x2], [y1, y2], 'k-', label='Línea entre P1 y P2')
plt.plot([x1, x3], [y1, y3], 'b--', label='Base del triángulo')
plt.plot([x3, x3], [y1, y3], 'g--', label='Altura del triángulo')


plt.scatter([x1, x2, x3], [y1, y2, y3], color='red')
plt.text(x1, y1 - 0.2, 'P1 (x1,y1)', ha='center')
plt.text(x2, y2 + 0.2, 'P2 (x2,y2)', ha='center')
plt.text(x3, y3 + 0.2, 'P3 (x3,y3)', ha='center')


plt.title('Ejemplo de Interpolación Lineal')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()
