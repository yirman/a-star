import random
# Importamos la clase Nodo desde astar.py para que compartan la misma estructura en memoria
from astar import Nodo

def generar_laberinto_completo(filas, columnas, tipo_laberinto="perfecto", factor_imperfecto=0.50):
    """Genera la matriz del laberinto usando celdas de tipo Nodo."""
    cuadricula = [[Nodo(f, c) for c in range(columnas)] for f in range(filas)]
    for f in range(filas):
        for c in range(columnas):
            cuadricula[f][c].tipo = "PARED"

    visitados = set()
    pila = []

    inicio_f, inicio_c = 1, 1
    cuadricula[inicio_f][inicio_c].tipo = "VACIO"
    visitados.add((inicio_f, inicio_c))
    pila.append((inicio_f, inicio_c))

    # Algoritmo de Backtracking (DFS)
    while pila:
        f_actual, c_actual = pila[-1]
        vecinos_candidatos = []
        movimientos = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        
        for df, dc in movimientos:
            nf, nc = f_actual + df, c_actual + dc
            if 0 < nf < filas - 1 and 0 < nc < columnas - 1:
                if (nf, nc) not in visitados:
                    vecinos_candidatos.append((nf, nc))

        if vecinos_candidatos:
            nf, nc = random.choice(vecinos_candidatos)
            pared_f = f_actual + (nf - f_actual) // 2
            pared_c = c_actual + (nc - c_actual) // 2
            cuadricula[pared_f][pared_c].tipo = "VACIO"
            cuadricula[nf][nc].tipo = "VACIO"
            visitados.add((nf, nc))
            pila.append((nf, nc))
        else:
            pila.pop()

    # Romper paredes si se pide un laberinto imperfecto
    if tipo_laberinto.lower() == "imperfecto":
        for f in range(1, filas - 1):
            for c in range(1, columnas - 1):
                if cuadricula[f][c].tipo == "PARED":
                    es_conector_h = (cuadricula[f][c-1].tipo == "VACIO" and cuadricula[f][c+1].tipo == "VACIO")
                    es_conector_v = (cuadricula[f-1][c].tipo == "VACIO" and cuadricula[f+1][c].tipo == "VACIO")
                    if es_conector_h or es_conector_v:
                        if random.random() < factor_imperfecto:
                            cuadricula[f][c].tipo = "VACIO"

    return cuadricula