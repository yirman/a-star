import random

class Nodo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = "VACIO"    # Puede ser: "VACIO", "PARED", "INICIO", "META"
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.padre = None

def generar_laberinto_completo(filas, columnas, tipo_laberinto="perfecto", factor_imperfecto=0.2):
    """
    Genera una matriz bidimensional de Nodos que representa un laberinto aleatorio.
    
    Parámetros:
    - filas, columnas: Dimensiones de la cuadrícula (deben ser impares para mejores resultados).
    - tipo_laberinto: "perfecto" o "imperfecto".
    - factor_imperfecto: Porcentaje de paredes a eliminar si el laberinto es imperfecto (0.0 a 1.0).
    """
    # 1. Inicializar la cuadrícula llena por completo de paredes.
    # El algoritmo de Backtracking irá tallando/abriendo caminos sobre este bloque sólido.
    cuadricula = [[Nodo(f, c) for c in range(columnas)] for f in range(filas)]
    for f in range(filas):
        for c in range(columnas):
            cuadricula[f][c].tipo = "PARED"

    # Estructuras auxiliares para el Backtracking (DFS)
    visitados = set()
    pila = []

    # Comenzamos la talla del laberinto desde una celda impar (ej. 1, 1) para mantener consistencia con los muros
    inicio_f, inicio_c = 1, 1
    cuadricula[inicio_f][inicio_c].tipo = "VACIO"
    visitados.add((inicio_f, inicio_c))
    pila.append((inicio_f, inicio_c))

    # 2. Algoritmo de Backtracking (DFS) para crear un Laberinto Perfecto
    while pila:
        f_actual, c_actual = pila[-1] # Miramos el nodo en el tope de la pila
        
        # Buscamos vecinos a una distancia de 2 celdas. 
        # Avanzar de 2 en 2 celdas asegura que siempre quede un muro grueso divisor entre pasillos.
        vecinos_candidatos = []
        movimientos = [(-2, 0), (2, 0), (0, -2), (0, 2)] # Arriba, Abajo, Izquierda, Derecha
        
        for df, dc in movimientos:
            nf, nc = f_actual + df, c_actual + dc
            # Verificar límites (dejando siempre un margen perimetral exterior de paredes)
            if 0 < nf < filas - 1 and 0 < nc < columnas - 1:
                if (nf, nc) not in visitados:
                    vecinos_candidatos.append((nf, nc))

        if vecinos_candidatos:
            # Seleccionamos un vecino al azar para garantizar la aleatoriedad del laberinto
            nf, nc = random.choice(vecinos_candidatos)
            
            # "Derribamos" la pared intermedia entre la celda actual y la celda elegida
            pared_f = f_actual + (nf - f_actual) // 2
            pared_c = c_actual + (nc - c_actual) // 2
            cuadricula[pared_f][pared_c].tipo = "VACIO"
            
            # Habilitamos la nueva celda como camino vacio
            cuadricula[nf][nc].tipo = "VACIO"
            
            # Registramos el progreso
            visitados.add((nf, nc))
            pila.append((nf, nc))
        else:
            # Si no hay vecinos sin visitar, retrocedemos en la pila (Backtrack)
            pila.pop()

    # 3. Transformación a Laberinto Imperfecto (si se solicita)
    # Rompemos paredes estratégicamente para crear bucles y rutas alternativas
    if tipo_laberinto.lower() == "imperfecto":
        for f in range(1, filas - 1):
            for c in range(1, columnas - 1):
                # Buscamos nodos que sigan siendo paredes interiores
                if cuadricula[f][c].tipo =="PARED":
                    # Evaluamos si derribar esta pared conecta dos pasillos independientes
                    # Conexión horizontal o Conexión vertical
                    es_conector_h = (cuadricula[f][c-1].tipo == "VACIO" and cuadricula[f][c+1].tipo == "VACIO")
                    es_conector_v = (cuadricula[f-1][c].tipo == "VACIO" and cuadricula[f+1][c].tipo == "VACIO")
                    
                    if es_conector_h or es_conector_v:
                        # Aplicamos la probabilidad basada en el factor_imperfecto
                        if random.random() < factor_imperfecto:
                            cuadricula[f][c].tipo = "VACIO"

    return cuadricula