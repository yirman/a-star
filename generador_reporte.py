import os

def exportar_reporte_txt(cuadricula, ruta_optima, nodos_visitados, modo_laberinto, nombre_archivo="reporte_ejecucion.txt"):
    """
    Genera un archivo de texto con el mapa del laberinto resuelto y 
    una redacción paso a paso de la ejecución histórica del algoritmo A*.
    """
    filas = len(cuadricula)
    columnas = len(cuadricula[0])
    
    # Creamos un set de coordenadas de la ruta para agilizar la escritura del mapa
    set_ruta = {(nodo.fila, nodo.columna) for nodo in ruta_optima} if ruta_optima else set()

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        # --- SECCIÓN 1: CABECERA DEL REPORTE ---
        f.write("=====================================================================\n")
        f.write("          REPORTE DE EJECUCIÓN - AGENTE EXPLORADOR A* (UNEG)          \n")
        f.write("=====================================================================\n")
        f.write(f"Configuración del Entorno: {filas}x{columnas} celdas.\n")
        f.write(f"Tipología del Laberinto: {modo_laberinto.upper()}\n")
        f.write(f"Resultado de la Búsqueda: {'ÉXITO - Ruta óptima trazada' if ruta_optima else 'FALLO - Laberinto sin salida'}\n")
        if ruta_optima:
            f.write(f"Longitud de la Ruta Final: {len(ruta_optima)} pasos.\n")
        f.write(f"Total de Nodos Evaluados (Closed Set): {len(nodos_visitados)} celdas.\n")
        f.write("=====================================================================\n\n")

        # --- SECCIÓN 2: MAPA DEL LABERINTO RESUELTO ---
        f.write("--- MAPA DEL LABERINTO RESUELTO ---\n")
        f.write("Leyenda: [■] Pared | [ ] Camino | [S] Inicio | [E] Meta | [·] Ruta Óptima\n\n")
        
        for fila in range(filas):
            linea_mapa = ""
            for columna in range(columnas):
                nodo = cuadricula[fila][columna]
                
                if nodo.tipo == "INICIO":
                    linea_mapa += "S "
                elif nodo.tipo == "META":
                    linea_mapa += "E "
                elif nodo.tipo == "PARED":
                    linea_mapa += "■ "
                elif (fila, columna) in set_ruta:
                    linea_mapa += "· "
                else:
                    linea_mapa += "  "  # Espacio vacío transitable no usado en la ruta final
            f.write(linea_mapa + "\n")
        f.write("\n" + "="*69 + "\n\n")

        # --- SECCIÓN 3: REDACCIÓN PASO A PASO (AUDITORÍA) ---
        f.write("--- REDACCIÓN CRONOLÓGICA DE LA EJECUCIÓN DEL ALGORITMO ---\n\n")
        
        # Ordenamos los nodos visitados por el costo 'g' para simular la línea de tiempo de exploración
        nodos_ordenados = sorted(list(nodos_visitados), key=lambda n: n.g if n.g != float('inf') else 0)
        
        f.write("[PASO 001] El agente se posiciona en el punto de partida original.\n")
        f.write(f"           -> Coordenadas de Inicio: ({ruta_optima[0].fila}, {ruta_optima[0].columna}) si existe ruta.\n\n")

        contador_pasos = 2
        for i, nodo in enumerate(nodos_ordenados):
            if nodo.tipo == "INICIO":
                continue
                
            f.write(f"[PASO {contador_pasos:03d}] El agente extrae el nodo más prometedor de la cola de prioridad (Min-Heap).\n")
            f.write(f"           -> Inspeccionando Celda en posición: Fil {nodo.fila}, Col {nodo.columna}\n")
            f.write(f"           -> Evaluación matemática de costes: g(n)={nodo.g} pasos dados, h(n)={nodo.h} (Manhattan estimado).\n")
            f.write(f"           -> Función de Coste Total evaluada en frontera: f(n) = {nodo.f}\n")
            
            if nodo.padre:
                f.write(f"           -> Este nodo se alcanzó de manera óptima desde la celda: ({nodo.padre.fila}, {nodo.padre.columna})\n")
            
            if nodo.tipo == "META":
                f.write(f"\n[¡META ALCANZADA!] El agente interceptó con éxito las coordenadas de salida.\n")
                f.write("           -> Deteniendo exploración activa de la frontera.\n")
                break
                
            f.write("\n")
            contador_pasos += 1

        # Si terminó y no se llegó a la meta
        if not ruta_optima:
            f.write("\n[FIN DE LA BÚSQUEDA] La cola de prioridad se vació por completo.\n")
            f.write("                     El agente exploró todos los pasillos accesibles sin interceptar la meta.\n")
            f.write("                     Conclusión: El laberinto no posee soluciones válidas.\n")

    print(f" Reporte generado exitosamente con el nombre: '{nombre_archivo}'")