import heapq

class Nodo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.g = float('inf')  # Costo desde el inicio hasta el nodo actual
        self.h = 0             # Estimación heurística hasta la meta
        self.f = float('inf')  # Costo total estimado: f(n) = g(n) + h(n)
        self.padre = None      # Rastro para reconstruir la ruta final

    # Definimos el operador "menor que" (<) para que la cola de prioridad 
    # ordene automáticamente los nodos evaluando primero el menor f(n)
    def __lt__(self, otro):
        return self.f < otro.f

def distancia_manhattan(nodo_a, nodo_b):
    """
    Calcula la distancia de Manhattan, ideal para movimientos en 
    cuadrículas donde no se permiten diagonales (4 direcciones).
    """
    return abs(nodo_a.fila - nodo_b.fila) + abs(nodo_a.columna - nodo_b.columna)

def obtener_vecinos(cuadriscula, nodo_actual):
    """
    Retorna los nodos adyacentes válidos (Arriba, Abajo, Izquierda, Derecha)
    que no sean paredes/obstáculos.
    """
    vecinos = []
    filas_totales = len(cuadriscula)
    columnas_totales = len(cuadriscula[0])

    # Definición de movimientos: (delta_fila, delta_columna)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha

    for df, dc in movimientos:
        nueva_f = nodo_actual.fila + df
        nueva_c = nodo_actual.columna + dc

        # Verificar límites de la cuadrícula
        if 0 <= nueva_f < filas_totales and 0 <= nueva_c < columnas_totales:
            vecino = cuadriscula[nueva_f][nueva_c]
            # Asumiendo que en tu matriz, el valor 1 (o un booleano) representa una pared
            # Modifica esta condición según cómo estructures tus obstáculos
            if vecino.tipo != "PARED": 
                vecinos.append(vecino)
                
    return vecinos

def reconstruir_ruta(nodo_meta):
    """
    Camina hacia atrás utilizando las referencias de los padres 
    para trazar el camino óptimo desde el inicio.
    """
    ruta = []
    actual = nodo_meta
    while actual is not None:
        ruta.append((actual.fila, actual.columna))
        actual = actual.padre
    return ruta[::-1]  # Invierte la lista para ir de Inicio -> Meta

def algoritmo_a_estrella(cuadriscula, inicio, meta):
    """
    Implementación del algoritmo A* diseñada para ejecutarse paso a paso
    o de forma lineal. 
    'cuadriscula' es una matriz bidimensional de objetos de tipo Nodo.
    """
    # 1. Inicialización
    frontera = []  # Open Set (Cola de prioridad)
    visitados = set()  # Closed Set (Conjunto para búsquedas O(1))

    # Configuración del nodo inicial
    inicio.g = 0
    inicio.h = distancia_manhattan(inicio, meta)
    inicio.f = inicio.g + inicio.h
    
    # Insertamos una tupla en el heap: (costo_f, objeto_nodo)
    heapq.heappush(frontera, (inicio.f, inicio))

    while frontera:
        # Extrae el nodo con el menor f(n)
        _, nodo_actual = heapq.heappop(frontera)

        # Si ya llegamos a la meta, retornamos la ruta final
        if nodo_actual == meta:
            return reconstruir_ruta(meta), visitados, frontera

        # Añadimos al conjunto de visitados (Closed Set)
        visitados.add(nodo_actual)

        # Evaluamos los vecinos de la celda actual
        vecinos = obtener_vecinos(cuadriscula, nodo_actual)
        for vecino in vecinos:
            if vecino in visitados:
                continue

            # El costo para moverse a un vecino en una cuadrícula regular es +1
            g_tentativo = nodo_actual.g + 1

            # Si encontramos un camino más corto hacia este vecino
            if g_tentativo < vecino.g:
                vecino.padre = nodo_actual
                vecino.g = g_tentativo
                vecino.h = distancia_manhattan(vecino, meta)
                vecino.f = vecino.g + vecino.h

                # Si no está en la frontera, lo añadimos
                # Para evitar duplicados en el heap, verificamos que no esté ya dentro
                if not any(vecino == item[1] for item in frontera):
                    heapq.heappush(frontera, (vecino.f, vecino))
                    
                    # NOTA PARA PYGAME: Aquí puedes marcar el nodo como 'FRONTERA'
                    # para que la interfaz lo pinte de un color específico en tiempo real.

        # NOTA PARA PYGAME: Aquí, después de procesar el nodo_actual, puedes marcarlo 
        # como 'VISITADO' y hacer un break temporal o yield si deseas pausar el bucle 
        # y renderizar el fotograma actual antes de seguir con el siguiente nodo.

    return None, visitados, frontera  # No se encontró un camino válido