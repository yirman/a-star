# Agente Explorador de Laberintos Autónomo basado en Algoritmo de Búsqueda Informada A* (A-Star)

Este repositorio contiene la implementación modular de un agente inteligente capaz de navegar y resolver laberintos autónomamente (tanto perfectos como imperfectos), visualizando el proceso de exploración matemática y su toma de decisiones en tiempo real. Desarrollado como proyecto práctico de evaluación para la cátedra de **Inteligencia Artificial**.

---

## 🛠️ Arquitectura Modular del Sistema

El software ha sido diseñado desacoplando por completo la lógica del negocio (estructuras de datos y algoritmos abstractos) de la interfaz gráfica y los mecanismos de persistencia de datos. El sistema está estructurado en cuatro módulos independientes:

1. **`a_star.py`**: Aloja la definición matemática de la clase `Nodo`, la función heurística basada en la geometría de Manhattan, y el núcleo del algoritmo $A^*$ implementado mediante un generador dinámico (`yield`) y una cola de prioridad basada en un montículo binario (`heapq`).
2. **`generador_laberinto.py`**: Contiene la lógica de generación procedimental de entornos basada en el algoritmo de Backtracking (Búsqueda en Profundidad o DFS) para esculpir laberintos perfectos, e incorpora un factor de aleatoriedad para romper ciclos y generar laberintos imperfectos con múltiples soluciones.
3. **`exportador.py`**: Módulo pasivo encargado de la persistencia y auditoría del sistema. Genera un reporte detallado en texto plano (`.txt`) que mapea el laberinto resuelto y redacta cronológicamente el análisis matemático de costos de cada celda procesada.
4. **`main_gui.py`**: Actúa como el orquestador o controlador principal del sistema. Inicializa el entorno gráfico mediante **Pygame**, administra el bucle de eventos de control por teclado, y renderiza visualmente el mapa y los costos numéricos en tiempo real.

---

## 🧠 Fundamentos Teóricos del Agente

### Algoritmo A*
El agente selecciona su ruta minimizando la función de evaluación clásica:
$$f(n) = g(n) + h(n)$$

* **$g(n)$**: Representa el coste real acumulado desde el nodo inicial hasta el nodo actual $n$. En nuestro entorno ortogonal uniforme, cada desplazamiento básico posee un coste unitario estricto de $1$.
* **$h(n)$**: Representa la función heurística informada que estima el coste restante desde el nodo $n$ hasta la meta.

### Heurística Admisible: Distancia de Manhattan
Dado que el entorno prohíbe terminantemente los desplazamientos diagonales (el agente solo puede moverse en los 4 puntos cardinales ortogonales), se utiliza de forma obligatoria la **Distancia de Manhattan**:
$$h(n) = |x_1 - x_2| + |y_1 - y_2|$$

Esta heurística es matemáticamente **admisible** (nunca sobreestima el coste real hacia la meta) y **consistente** (cumple con la desigualdad triangular), lo que garantiza de manera absoluta que el algoritmo $A^*$ interceptará la ruta óptima más corta sin incurrir en una exploración redundante o a ciegas.

---

## 🎨 Características de la Interfaz Visual y Renderizado de Costos

El entorno visual de Pygame muestra dinámicamente los estados del algoritmo basándose en una paleta cromática profesional y descriptiva:

* 🔵 **Inicio (Azul)**: Punto de partida inicial del agente explorer (`cuadricula[1][1]`).
* 🟣 **Meta (Morado)**: Coordenadas de salida del laberinto (`cuadricula[FILAS-2][COLUMNAS-2]`).
* ⬛ **Pared (Gris Oscuro)**: Obstáculo infranqueable.
* 🟢 **Frontera / Open Set (Verde)**: Nodos descubiertos cuyos costes ya fueron calculados y se encuentran ordenados en la cola de prioridad a la espera de ser evaluados.
* 🔴 **Visitados / Closed Set (Rojo)**: Nodos ya extraídos de la raíz del montículo binario y procesados a fondo por el agente.
* 🟡 **Ruta Final (Amarillo)**: El camino óptimo definitivo trazado en reversa mediante los punteros padres al alcanzar la meta.

### 🔢 Desglose Numérico en Celda (Rúbrica del Proyecto)
Cumpliendo estrictamente con los requerimientos visuales del laboratorio, cada celda explorada (perteneciente a la frontera o al conjunto cerrado) renderiza internamente tres valores numéricos clave en sus esquinas:
* **Esquina Superior Izquierda**: Coste Total $F$.
* **Esquina Inferior Izquierda**: Coste Acumulado $G$ (Pasos dados).
* **Esquina Inferior Derecha**: Coste Estimado $H$ (Heurística Manhattan).

---

## ⌨️ Controles Interactivos del Sistema

Al ejecutar el orquestador principal (`main_gui.py`), el usuario puede controlar de forma interactiva todo el ciclo de vida del agente mediante las siguientes teclas:

* **`[ESPACIO]`**: Inicia la animación de búsqueda paso a paso del algoritmo $A^*$.
* **`[P]`**: Genera instantáneamente un nuevo laberinto aleatorio de tipo **Perfecto** (un único camino matemático libre de ciclos).
* **`[I]`**: Genera un nuevo laberinto aleatorio de tipo **Imperfecto** (rompe paredes seleccionadas al azar para habilitar rutas alternativas).
* **`[R]`**: Reinicia por completo el estado de búsqueda actual (limpia los conjuntos abierto, cerrado y los costos de los nodos) manteniendo la misma topografía del laberinto para repetir la prueba.
* **`[A]`**: Conmuta (activa o desactiva) el flag de **Auto-Apertura del Reporte**. Si se establece en `SÍ`, el sistema operativo abrirá el bloc de notas automáticamente con la bitácora técnica al finalizar la ruta.

---

## 📊 Sistema de Auditoría y Persistencia (`.txt`)

Al finalizar con éxito o fallo la exploración, el módulo `exportador.py` genera de forma automatizada un reporte físico denominado `reporte_ejecucion.txt`. Este archivo de texto contiene:
1. **Metadata Ejecutiva**: Tamaño de la matriz, tipo de laberinto, número de celdas evaluadas a fondo en el *Closed Set* y longitud exacta de la ruta final óptima.
2. **Mapa de Texto Plano**: Representación ascii/unicode legible por humanos del entorno resuelto, diferenciando las paredes de la ruta óptima mediante caracteres especiales.
3. **Bitácora Cronológica**: Desglose paso a paso del recorrido matemático del agente, detallando las coordenadas de cada nodo extraído del Min-Heap, su procedencia y la validación formal de sus funciones de coste ($f = g + h$).

---

## 🚀 Requisitos e Instalación

### Requisitos Previos
* **Python 3.8 o superior**
* **Pygame**

### Instalación de Dependencias
Asegúrate de instalar la librería gráfica antes de ejecutar el programa:
```bash
pip install pygame