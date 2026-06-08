import pygame
import sys

# Importamos la clase Nodo y el algoritmo desde astar.py
from astar import Nodo, algoritmo_a_estrella_paso_a_paso, distancia_manhattan

# Importamos la función de generación desde generador_laberinto.py
# Nota: Si tu archivo usa guion medio, Python no permite importarlo directamente de forma nativa.
# Te sugiero renombrar "generador-laberinto.py" a "generador_laberinto.py" (con guion bajo).
from generador_laberinto import generar_laberinto_completo

# Importamos el mecanismo de persistencia de datos sin tocar la lógica de negocio
from generador_reporte import exportar_reporte_txt

# --- CONFIGURACIÓN DE LA INTERFAZ ---
ANCHO_PANEL_CONTROL = 150
DIMENSION_CELDA = 35  # Tamaño de cada cuadrícula en píxeles

# Dimensiones del laberinto (Deben ser impares)
FILAS = 19
COLUMNAS = 19

# Colores (RGB)
COLOR_PARED = (33, 47, 61)       # Gris oscuro
COLOR_VACIO = (255, 255, 255)     # Blanco
COLOR_INICIO = (41, 128, 185)    # Azul
COLOR_META = (155, 89, 182)      # Morado
COLOR_FRONTERA = (46, 204, 113)  # Verde brillante (Open Set)
COLOR_VISITADO = (231, 76, 60)   # Rojo/Naranja (Closed Set)
COLOR_RUTA = (241, 196, 15)      # Amarillo (Ruta Final)
COLOR_FONDO_PANEL = (242, 243, 244)
COLOR_TEXTO = (44, 62, 80)
COLOR_TEXTO_COSTOS = (28, 40, 51) # Gris muy oscuro para legibilidad numérica

def dibujar_interfaz(pantalla, cuadricula, ruta, visitados, frontera, modo_laberinto, alto_ventana, auto_abrir_reporte):
    pantalla.fill(COLOR_VACIO)

    # Inicializar fuente pequeña para los costos internos de las celdas
    fuente_costos = pygame.font.SysFont("Arial", 9, bold=True)

    # 1. Dibujar el Laberinto / Cuadrícula
    for f in range(FILAS):
        for c in range(COLUMNAS):
            nodo = cuadricula[f][c]
            x_celda = c * DIMENSION_CELDA
            y_celda = f * DIMENSION_CELDA
            rectangulo = pygame.Rect(c * DIMENSION_CELDA, f * DIMENSION_CELDA, DIMENSION_CELDA, DIMENSION_CELDA)

            # Determinar color según el tipo base o su estado en las estructuras
            if nodo.tipo == "PARED":
                color = COLOR_PARED
            elif nodo.tipo == "INICIO":
                color = COLOR_INICIO
            elif nodo.tipo == "META":
                color = COLOR_META
            else:
                if ruta and nodo in ruta:
                    color = COLOR_RUTA
                elif nodo in frontera:
                    color = COLOR_FRONTERA
                elif nodo in visitados:
                    color = COLOR_VISITADO
                else:
                    color = COLOR_VACIO

            pygame.draw.rect(pantalla, color, rectangulo)
            pygame.draw.rect(pantalla, (210, 210, 210), rectangulo, 1)  # Retícula sutil

            # --- NUEVA SECCIÓN: RENDERIZADO DE COSTOS F, G, H INTERNOS ---
            # Solo dibujamos texto si la celda ha sido descubierta y sus costos calculados (no son infinitos)
            if nodo.tipo in ["VACIO", "INICIO", "META"] and nodo.f != float('inf') and nodo.tipo != "PARED":
                # Arriba-Izquierda -> F = G + H
                txt_f = fuente_costos.render(str(int(nodo.f)), True, COLOR_TEXTO_COSTOS)
                pantalla.blit(txt_f, (x_celda + 3, y_celda + 2))

                # Abajo-Izquierda -> G (Pasos recorridos)
                txt_g = fuente_costos.render(str(int(nodo.g)), True, COLOR_TEXTO_COSTOS)
                pantalla.blit(txt_g, (x_celda + 3, y_celda + DIMENSION_CELDA - 12))

                # Abajo-Derecha -> H (Heurística Manhattan)
                txt_h = fuente_costos.render(str(int(nodo.h)), True, COLOR_TEXTO_COSTOS)
                # Cálculo de posición dinámica a la derecha restando el ancho del texto renderizado
                pantalla.blit(txt_h, (x_celda + DIMENSION_CELDA - txt_h.get_width() - 3, y_celda + DIMENSION_CELDA - 12))

    # 2. Dibujar Panel de Control Lateral
    x_panel = COLUMNAS * DIMENSION_CELDA
    panel_rect = pygame.Rect(x_panel, 0, ANCHO_PANEL_CONTROL, alto_ventana)
    pygame.draw.rect(pantalla, COLOR_FONDO_PANEL, panel_rect)

    fuente = pygame.font.SysFont("Arial", 14)
    fuente_negrita = pygame.font.SysFont("Arial", 14, bold=True)

    instrucciones = [
        ("CONTROLES", True),
        ("[ESPACIO] Buscar", False),
        ("[P] Lab. Perfecto", False),
        ("[I] Lab. Imperfecto", False),
        ("[R] Reiniciar A*", False),
        ("[A] Auto-Abrir Reporte", False), # Nueva línea visual de control
        ("", False),
        (f"Modo: {modo_laberinto.upper()}", True),
        (f"Auto-Abrir-Reporte: {'SÍ' if auto_abrir_reporte else 'NO'}", True), # Muestra el estado actual
    ]

    y_offset = 20
    for texto, es_negrita in instrucciones:
        if texto == "":
            y_offset += 15
            continue
        render_texto = fuente_negrita.render(texto, True, COLOR_TEXTO) if es_negrita else fuente.render(texto, True, COLOR_TEXTO)
        pantalla.blit(render_texto, (x_panel + 10, y_offset))
        y_offset += 25

    # 3. Dibujar Leyenda de Colores
    y_offset += 20
    leyenda = [
        ("Inicio", COLOR_INICIO),
        ("Meta", COLOR_META),
        ("Pared", COLOR_PARED),
        ("Frontera", COLOR_FRONTERA),
        ("Visitado", COLOR_VISITADO),
        ("Ruta Final", COLOR_RUTA)
    ]

    for texto, color in leyenda:
        pygame.draw.rect(pantalla, color, (x_panel + 10, y_offset, 15, 15))
        render_txt = fuente.render(texto, True, COLOR_TEXTO)
        pantalla.blit(render_txt, (x_panel + 35, y_offset))
        y_offset += 25

def main():
    pygame.init()
    pygame.display.set_caption("Visualizador Algoritmo A* - UNEG")
    
    ancho_total = (COLUMNAS * DIMENSION_CELDA) + ANCHO_PANEL_CONTROL
    alto_total = FILAS * DIMENSION_CELDA
    pantalla = pygame.display.set_mode((ancho_total, alto_total))
    reloj = pygame.time.Clock()

    modo_laberinto = "perfecto"
    # Llamamos a la función alojada en generador_laberinto.py
    cuadricula = generar_laberinto_completo(FILAS, COLUMNAS, modo_laberinto)

    inicio_nodo = cuadricula[1][1]
    inicio_nodo.tipo = "INICIO"
    meta_nodo = cuadricula[FILAS-2][COLUMNAS-2]
    meta_nodo.tipo = "META"

    generador_a_star = None
    animacion_activa = False
    busqueda_finalizada = False

    ruta_optima = []
    nodos_visitados = set()
    nodos_frontera = []

    auto_abrir_reporte = False

    while True:
        reloj.tick(30)  # Velocidad de la animación (FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # [ESPACIO] -> Iniciar la búsqueda importada paso a paso
                if evento.key == pygame.K_SPACE and not animacion_activa and not busqueda_finalizada:
                    for fila in cuadricula:
                        for nodo in fila:
                            nodo.reset_busqueda()
                    generador_a_star = algoritmo_a_estrella_paso_a_paso(cuadricula, inicio_nodo, meta_nodo)
                    animacion_activa = True

                # [P] -> Nuevo Laberinto Perfecto
                if evento.key == pygame.K_p:
                    animacion_activa = False
                    busqueda_finalizada = False
                    modo_laberinto = "perfecto"
                    cuadricula = generar_laberinto_completo(FILAS, COLUMNAS, modo_laberinto)
                    inicio_nodo = cuadricula[1][1]
                    inicio_nodo.tipo = "INICIO"
                    meta_nodo = cuadricula[FILAS-2][COLUMNAS-2]
                    meta_nodo.tipo = "META"
                    ruta_optima, nodos_frontera = [], []
                    nodos_visitados.clear()

                # [I] -> Nuevo Laberinto Imperfecto
                if evento.key == pygame.K_i:
                    animacion_activa = False
                    busqueda_finalizada = False
                    modo_laberinto = "imperfecto"
                    cuadricula = generar_laberinto_completo(FILAS, COLUMNAS, modo_laberinto)
                    inicio_nodo = cuadricula[1][1]
                    inicio_nodo.tipo = "INICIO"
                    meta_nodo = cuadricula[FILAS-2][COLUMNAS-2]
                    meta_nodo.tipo = "META"
                    ruta_optima, nodos_frontera = [], []
                    nodos_visitados.clear()

                # [R] -> Reiniciar estado de búsqueda manteniendo el mapa
                if evento.key == pygame.K_r:
                    animacion_activa = False
                    busqueda_finalizada = False
                    ruta_optima, nodos_frontera = [], []
                    nodos_visitados.clear()
                    for fila in cuadricula:
                        for nodo in fila:
                            nodo.reset_busqueda()
                
                # [A] -> Conmuta (habilita/deshabilita) la apertura automática del TXT
                if evento.key == pygame.K_a:
                    auto_abrir_reporte = not auto_abrir_reporte

        # Avanzar el frame de la animación del algoritmo
        if animacion_activa and generador_a_star:
            try:
                ruta, visitados, frontera, finalizado = next(generador_a_star)
                nodos_visitados = visitados
                nodos_frontera = frontera
                
                if finalizado:
                    animacion_activa = False
                    busqueda_finalizada = True
                    if ruta:
                        ruta_optima = ruta
                    
                    # =========================================================================
                    # UNIENDO EL COPIADO DE DATOS: Llama al exportador al finalizar la búsqueda
                    # =========================================================================
                    exportar_reporte_txt(cuadricula, ruta_optima, nodos_visitados, modo_laberinto, auto_abrir_reporte)
                    # =========================================================================

            except StopIteration:
                animacion_activa = False
                busqueda_finalizada = True

        # Renderizar la pantalla pasando los datos de los tres archivos combinados
        dibujar_interfaz(pantalla, cuadricula, ruta_optima, nodos_visitados, nodos_frontera, modo_laberinto, alto_total, auto_abrir_reporte)
        pygame.display.update()

if __name__ == "__main__":
    main()