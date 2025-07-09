import random

# Definir los patrones o "tiles" y las reglas de adyacencia
TILES = {
    "Agua": {"admite": ["Agua", "Arena"]},
    "Arena": {"admite": ["Agua", "Arena", "Hierba"]},
    "Hierba": {"admite": ["Arena", "Hierba"]}
}

# Tamaño de la cuadrícula
WIDTH = 5
HEIGHT = 5

# Inicializar la cuadrícula con todas las posibles opciones en cada celda
def inicializar_cuadricula():
    cuadricula = [[list(TILES.keys()) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    return cuadricula

# Mostrar el estado actual de la cuadrícula
def mostrar_cuadricula(cuadricula):
    for fila in cuadricula:
        fila_colapsada = [celda[0] if len(celda) == 1 else "?" for celda in fila]
        print(" | ".join(fila_colapsada))
    print()

# Seleccionar una celda con la menor entropía (menos opciones posibles)
def seleccionar_celda(cuadricula):
    opciones_minimas = float('inf')
    celda_seleccionada = None
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if 1 < len(cuadricula[y][x]) < opciones_minimas:
                opciones_minimas = len(cuadricula[y][x])
                celda_seleccionada = (x, y)
    return celda_seleccionada

# Colapsar una celda seleccionada a un patrón aleatorio
def colapsar_celda(cuadricula, x, y):
    if len(cuadricula[y][x]) > 1:
        cuadricula[y][x] = [random.choice(cuadricula[y][x])]

# Propagar restricciones a las celdas adyacentes
def propagar(cuadricula, x, y):
    tile_actual = cuadricula[y][x][0]

    # Verificar celdas adyacentes y restringir sus posibles opciones
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and len(cuadricula[ny][nx]) > 1:
            opciones_validas = [tile for tile in cuadricula[ny][nx] if tile in TILES[tile_actual]["admite"]]
            if opciones_validas:
                cuadricula[ny][nx] = opciones_validas

# Ejecutar el algoritmo de colapso de onda
def ejecutar_wfc():
    cuadricula = inicializar_cuadricula()
    mostrar_cuadricula(cuadricula)

    while any(len(celda) > 1 for fila in cuadricula for celda in fila):
        # Seleccionar la celda con menor entropía
        seleccion = seleccionar_celda(cuadricula)
        if seleccion is None:
            break  # Todas las celdas están colapsadas

        x, y = seleccion

        # Colapsar la celda seleccionada
        colapsar_celda(cuadricula, x, y)

        # Propagar las restricciones
        propagar(cuadricula, x, y)

        # Mostrar el estado actual de la cuadrícula
        mostrar_cuadricula(cuadricula)

# Ejecutar el algoritmo de colapso de onda
ejecutar_wfc()
