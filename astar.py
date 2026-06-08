import heapq

class Nodo:
    """
    Representa una celda individual dentro de la cuadrícula del laberinto.
    Almacena su ubicación física y las variables de coste de la búsqueda informada.
    """
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = "VACIO"    # Estado base de la celda: VACIO, PARED, INICIO o META
        self.g = float('inf')  # Coste real acumulado desde el nodo de inicio hasta este nodo
        self.h = 0             # Coste estimado (heurística) desde este nodo hasta la meta
        self.f = float('inf')  # Función de coste total: f(n) = g(n) + h(n) [cite: 30]
        self.padre = None      # Puntero de retorno para reconstruir el camino óptimo

    def __lt__(self, otro):
        """
        Sobrecarga del operador 'menor que' (<). Es crucial para que la cola de prioridad
        (heapq) pueda ordenar los objetos Nodo automáticamente basándose en su valor f(n),
        garantizando que el nodo con menor coste estimado siempre suba a la raíz.
        """
        return self.f < otro.f

    def reset_busqueda(self):
        """
        Restablece los parámetros del algoritmo a su estado inicial.
        Permite limpiar mapas y repetir simulaciones sin alterar la topología de las paredes.
        """
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.padre = None

def distancia_manhattan(nodo_a, nodo_b):
    """
    Función Heurística h(n) basada en la geometría de Taxistas o Manhattan[cite: 17, 36].
    Mide la distancia ortogonal absoluta entre dos puntos. Al no permitir movimientos
    diagonales en el laberinto, esta heurística es admisible y consistente, lo que significa
    que jamás sobreestimará el coste real y guiará al algoritmo de forma óptima hacia la meta.
    """
    return abs(nodo_a.fila - nodo_b.fila) + abs(nodo_a.columna - nodo_b.columna)

def obtener_vecinos(cuadricula, nodo_actual):
    """
    Inspecciona los 4 puntos cardinales adyacentes al nodo actual.
    Filtra y descarta las celdas que se salen de la matriz o que representan un obstáculo.
    """
    vecinos = []
    filas_totales = len(cuadricula)
    columnas_totales = len(cuadricula[0])
    
    # Desplazamientos ortogonales: Arriba, Abajo, Izquierda, Derecha
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for df, dc in movimientos:
        nueva_f = nodo_actual.fila + df
        nueva_c = nodo_actual.columna + dc

        # Validar límites fronterizos de la matriz bidimensional
        if 0 <= nueva_f < filas_totales and 0 <= nueva_c < columnas_totales:
            vecino = cuadricula[nueva_f][nueva_c]
            # Restricción: El agente solo puede transitar por zonas libres
            if vecino.tipo != "PARED": 
                vecinos.append(vecino)
    return vecinos

def reconstruir_ruta(nodo_meta):
    """
    Trazado inverso del camino. Camina en reversa desde el nodo meta saltando de
    padre en padre hasta alcanzar el nodo origen, invirtiendo la lista al final
    para trazar la secuencia en orden cronológico correcto (Inicio -> Meta)[cite: 13].
    """
    ruta = []
    actual = nodo_meta
    while actual is not None:
        ruta.append(actual)
        actual = actual.padre
    return ruta[::-1] # Inversión de la lista mediante slicing de Python

def algoritmo_a_estrella_paso_a_paso(cuadricula, inicio, meta):
    """
    Implementación dinámica del algoritmo A* configurada como un Generador de Python.
    Utiliza la palabra clave 'yield' para transferir el control y los datos a la interfaz gráfica
    en cada ciclo, logrando animar el proceso de exploración en tiempo real de forma limpia[cite: 13].
    """
    # Inicialización de las estructuras de datos clave
    frontera = []      # Open Set: Cola de prioridad que contiene los nodos por evaluar
    visitados = set()  # Closed Set: Conjunto hash de nodos ya procesados (búsquedas en tiempo O(1))

    # Configuración del estado inicial del punto de partida
    inicio.g = 0
    inicio.h = distancia_manhattan(inicio, meta)
    inicio.f = inicio.g + inicio.h
    
    # Se introduce el nodo inicial en el heap empaquetado como una tupla: (prioridad_f, objeto_nodo)
    heapq.heappush(frontera, (inicio.f, inicio))

    while frontera:
        # Extrae de la frontera el nodo con el coste f(n) más bajo del conjunto actual
        _, nodo_actual = heapq.heappop(frontera)

        # CONDICIÓN DE VICTORIA: Si el nodo extraído coincide con el objetivo, la ruta óptima está asegurada
        if nodo_actual == meta:
            ruta_final = reconstruir_ruta(meta)
            # Retorna el tuple final marcando el flag de finalización en True
            yield (ruta_final, visitados, [item[1] for item in frontera], True)
            return

        # El nodo pasa formalmente al conjunto cerrado para evitar reevaluaciones redundantes
        visitados.add(nodo_actual)

        # Análisis de los nodos adyacentes hábiles
        vecinos = obtener_vecinos(cuadricula, nodo_actual)
        for vecino in vecinos:
            # Si el vecino ya fue evaluado a fondo, se ignora por completo
            if vecino in visitados:
                continue

            # Cálculo del coste g tentativo. En cuadrículas ortogonales uniformes, el coste de paso es 1
            g_tentativo = nodo_actual.g + 1

            # Si este camino ofrece un costo menor al que ya tenía registrado el vecino anteriormente
            if g_tentativo < vecino.g:
                # Se actualiza el árbol de procedencia del nodo
                vecino.padre = nodo_actual
                
                # Cálculo y asignación formal de las funciones matemáticas
                vecino.g = g_tentativo
                vecino.h = distancia_manhattan(vecino, meta)
                vecino.f = vecino.g + vecino.h

                # Si el vecino no está registrado en la lista de espera, se introduce en la frontera
                if not any(vecino == item[1] for item in frontera):
                    heapq.heappush(frontera, (vecino.f, vecino))

        # CONEXIÓN GUI: Transmite el estado actual del mapa al ciclo principal de Pygame
        # Permite pintar el Open Set y el Closed Set de este frame antes de procesar el siguiente nodo [cite: 13, 25]
        yield (None, visitados, [item[1] for item in frontera], False)

    # Si la frontera se vacía por completo y no se interceptó la meta, el laberinto no tiene salida
    yield (None, visitados, [], True)