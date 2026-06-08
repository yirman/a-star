import heapq

class Nodo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = "VACIO"    # Puede ser: VACIO, PARED, INICIO, META
        self.g = float('inf')  # Costo desde el inicio
        self.h = 0             # Heurística
        self.f = float('inf')  # Costo total f(n) = g(n) + h(n)
        self.padre = None      # Para reconstruir el camino

    def __lt__(self, otro):
        return self.f < otro.f

    def reset_busqueda(self):
        """Limpia los costos sin borrar si la celda es PARED, INICIO o META."""
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.padre = None

def distancia_manhattan(nodo_a, nodo_b):
    return abs(nodo_a.fila - nodo_b.fila) + abs(nodo_a.columna - nodo_b.columna)

def obtener_vecinos(cuadricula, nodo_actual):
    vecinos = []
    filas_totales = len(cuadricula)
    columnas_totales = len(cuadricula[0])
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha

    for df, dc in movimientos:
        nueva_f = nodo_actual.fila + df
        nueva_c = nodo_actual.columna + dc

        if 0 <= nueva_f < filas_totales and 0 <= nueva_c < columnas_totales:
            vecino = cuadricula[nueva_f][nueva_c]
            if vecino.tipo != "PARED": 
                vecinos.append(vecino)
    return vecinos

def reconstruir_ruta(nodo_meta):
    ruta = []
    actual = nodo_meta
    while actual is not None:
        ruta.append(actual)
        actual = actual.padre
    return ruta[::-1]

def algoritmo_a_estrella_paso_a_paso(cuadricula, inicio, meta):
    """
    Versión generadora del algoritmo A*. 
    Devuelve el estado actual de las listas en cada iteración para la GUI.
    """
    frontera = []  # Open Set
    visitados = set()  # Closed Set

    inicio.g = 0
    inicio.h = distancia_manhattan(inicio, meta)
    inicio.f = inicio.g + inicio.h
    heapq.heappush(frontera, (inicio.f, inicio))

    while frontera:
        _, nodo_actual = heapq.heappop(frontera)

        # Si encontramos la meta, devolvemos la ruta final y marcamos True (Finalizado)
        if nodo_actual == meta:
            ruta_final = reconstruir_ruta(meta)
            yield (ruta_final, visitados, [item[1] for item in frontera], True)
            return

        visitados.add(nodo_actual)

        vecinos = obtener_vecinos(cuadricula, nodo_actual)
        for vecino in vecinos:
            if vecino in visitados:
                continue

            g_tentativo = nodo_actual.g + 1

            if g_tentativo < vecino.g:
                vecino.padre = nodo_actual
                vecino.g = g_tentativo
                vecino.h = distancia_manhattan(vecino, meta)
                vecino.f = vecino.g + vecino.h

                if not any(vecino == item[1] for item in frontera):
                    heapq.heappush(frontera, (vecino.f, vecino))

        # Entregamos los datos actuales a la GUI para que los pinte en este frame, marcando False (No finalizado)
        yield (None, visitados, [item[1] for item in frontera], False)

    yield (None, visitados, [], True)  # Terminó el bucle sin encontrar solución