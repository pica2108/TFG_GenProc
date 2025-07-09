def actualizar_matriz(duplas, matriz):
    # Mapeo para unificar valores según las duplas
    mapeo = {}

    for a, b in duplas:
        # Si 'a' ya fue actualizado antes, usa el valor actualizado
        valor_a = mapeo.get(a, matriz[a // len(matriz)][a % len(matriz)])

        # Actualiza el valor en la posición 'b'
        mapeo[b] = valor_a

    # Aplicar los cambios a la matriz
    for key, value in mapeo.items():
        matriz[key // len(matriz)][key % len(matriz)] = value

    return matriz


# Ejemplo de uso
matriz = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

duplas = [(3, 5), (3, 6), (3, 8), (5, 6), (5, 8), (6, 8)]
resultado = actualizar_matriz(duplas, matriz)

for fila in resultado:
    print(fila)
