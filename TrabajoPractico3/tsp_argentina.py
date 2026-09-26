import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# =============================================================================
# TRABAJO PRÁCTICO N°3 - PROBLEMA DEL VIAJANTE (TSP)
# Capitales de provincias de la República Argentina
# =============================================================================

# 23 capitales provinciales (sin CABA, que no es provincia)
# Índice 0..22 (internamente), presentados al usuario como 1..23
PROVINCIAS = [
    "Córdoba",               # 0
    "Corrientes",            # 1
    "Formosa",               # 2
    "La Plata",              # 3
    "La Rioja",              # 4
    "Mendoza",               # 5
    "Neuquén",               # 6
    "Paraná",                # 7
    "Posadas",               # 8
    "Rawson",                # 9
    "Resistencia",           # 10
    "Río Gallegos",          # 11
    "S.F.V. de Catamarca",   # 12
    "S.M. de Tucumán",       # 13
    "S.S. de Jujuy",         # 14
    "Salta",                 # 15
    "San Juan",              # 16
    "San Luis",              # 17
    "Santa Fe",              # 18
    "Santa Rosa",            # 19
    "Sgo. del Estero",       # 20
    "Ushuaia",               # 21
    "Viedma",                # 22
]

NUM_CIUDADES = len(PROVINCIAS)   # 23

# Coordenadas geográficas (latitud, longitud) para graficar el mapa
COORDENADAS = [
    (-31.4201, -64.1888),   # 0  Córdoba
    (-27.4692, -58.8306),   # 1  Corrientes
    (-26.1775, -58.1781),   # 2  Formosa
    (-34.9214, -57.9545),   # 3  La Plata
    (-29.4131, -66.8558),   # 4  La Rioja
    (-32.8908, -68.8272),   # 5  Mendoza
    (-38.9516, -68.0591),   # 6  Neuquén
    (-31.7319, -60.5288),   # 7  Paraná
    (-27.3671, -55.8961),   # 8  Posadas
    (-43.3002, -65.1023),   # 9  Rawson
    (-27.4606, -58.9839),   # 10 Resistencia
    (-51.6226, -69.2181),   # 11 Río Gallegos
    (-28.4696, -65.7852),   # 12 Catamarca
    (-26.8241, -65.2226),   # 13 Tucumán
    (-24.1858, -65.2995),   # 14 Jujuy
    (-24.7821, -65.4232),   # 15 Salta
    (-31.5375, -68.5364),   # 16 San Juan
    (-33.2950, -66.3356),   # 17 San Luis
    (-31.6333, -60.7000),   # 18 Santa Fe
    (-36.6167, -64.2833),   # 19 Santa Rosa
    (-27.7951, -64.2615),   # 20 Sgo. del Estero
    (-54.8019, -68.3030),   # 21 Ushuaia
    (-40.8135, -62.9967),   # 22 Viedma
]

# ─────────────────────────────────────────────────────────────────────────────
# MATRIZ DE DISTANCIAS (en km, en línea recta)
# Fuente: Tabla de Distancias proporcionada en el enunciado del TP.
# ─────────────────────────────────────────────────────────────────────────────
#  Orden de las ciudades (columnas y filas):
#   0-COR  1-CTS  2-FOR  3-LP   4-LR   5-MZA  6-NQN  7-PAR  8-POS  9-RAW
#  10-RES 11-RG  12-CAT 13-TUC 14-JUJ 15-SAL 16-SJ  17-SL  18-SF  19-SR
#  20-SGO 21-USH 22-VMA
# ─────────────────────────────────────────────────────────────────────────────

DISTANCIAS = [
    #  COR   CTS   FOR    LP    LR   MZA   NQN   PAR   POS   RAW   RES    RG   CAT   TUC   JUJ   SAL    SJ    SL    SF    SR   SGO   USH   VMA
    [    0,  677,  824,  698,  340,  466,  907,  348,  919, 1321,  669, 2281,  362,  517,  809,  745,  412,  293,  330,  577,  401, 2618, 1047],  #  0 Córdoba
    [  677,    0,  157,  830,  814, 1131, 1534,  500,  291, 1845,   13, 2819,  691,  633,  742,  719, 1039,  969,  498, 1136,  535, 3131, 1532],  #  1 Corrientes
    [  824,  157,    0,  968,  927, 1269, 1690,  656,  263, 1999,  161, 2974,  793,  703,  750,  741, 1119, 1117,  654, 1293,  629, 3284, 1681],  #  2 Formosa
    [  698,  830,  968,    0, 1038, 1029, 1005,  427,  857, 1116,  833, 2064, 1030, 1132, 1385, 1333, 1053,  795,  444,  601,  991, 2350,  789],  #  3 La Plata
    [  340,  814,  927, 1038,    0,  427, 1063,  659, 1053, 1548,  802, 2473,  149,  330,  600,  533,  283,  435,  640,  834,  311, 2811, 1311],  #  4 La Rioja
    [  466, 1131, 1269, 1029,  427,    0,  676,  790, 1306, 1201, 1121, 2081,  569,  756, 1023,  957,  152,  265,  775,  586,  705, 2435, 1019],  #  5 Mendoza
    [  907, 1534, 1690, 1005, 1063,  676,    0, 1053, 1709,  543, 1530, 1412, 1184, 1374, 1662, 1595,  826,  648, 1052,  421, 1289, 1763,  479],  #  6 Neuquén
    [  348,  500,  656,  427,  659,  790, 1053,    0,  658, 1345,  498, 2320,  622,  707,  959,  906,  757,  574,   19,  642,  566, 2635, 1030],  #  7 Paraná
    [  919,  291,  263,  857, 1053, 1306, 1709,  658,    0, 1951,  305, 2914,  979,  924, 1007,  992, 1306, 1200,  664, 1293,  827, 3207, 1624],  #  8 Posadas
    [ 1321, 1845, 1999, 1116, 1548, 1201,  543, 1345, 1951,    0, 1843,  975, 1647, 1832, 2120, 2054, 1340, 1113, 1349,  745, 1721, 1300,  327],  #  9 Rawson
    [  669,   13,  161,  833,  802, 1121, 1530,  498,  305, 1843,    0, 2818,  678,  620,  729,  706, 1029,  958,  495, 1132,  521, 3131, 1526],  # 10 Resistencia
    [ 2281, 2819, 2974, 2064, 2473, 2081, 1412, 2320, 2914,  975, 2818,    0, 2587, 2773, 3063, 2997, 2231, 2046, 2325, 1712, 2677, 1359, 1294],  # 11 Río Gallegos
    [  362,  691,  793, 1030,  149,  569, 1184,  622,  979, 1647,  678, 2587,    0,  189,  477,  410,  430,  540,  602,  915,  166, 2931, 1391],  # 12 Catamarca
    [  517,  633,  703, 1132,  330,  756, 1374,  707,  924, 1832,  620, 2773,  189,    0,  293,  228,  612,  727,  689, 1088,  141, 3116, 1562],  # 13 Tucumán
    [  809,  742,  750, 1385,  600, 1023, 1662,  959, 1007, 2120,  729, 3063,  477,  293,    0,   67,  874, 1017,  942, 1382,  414, 3408, 1855],  # 14 Jujuy
    [  745,  719,  741, 1333,  533,  957, 1595,  906,  992, 2054,  706, 2997,  410,  228,   67,    0,  808,  950,  889, 1316,  353, 3341, 1790],  # 15 Salta
    [  412, 1039, 1119, 1053,  283,  152,  826,  757, 1306, 1340, 1029, 2231,  430,  612,  874,  808,    0,  284,  740,  686,  583, 2585, 1141],  # 16 San Juan
    [  293,  969, 1117,  795,  435,  265,  648,  574, 1200, 1113,  958, 2046,  540,  727, 1017,  950,  284,    0,  560,  412,  643, 2392,  882],  # 17 San Luis
    [  330,  498,  654,  444,  640,  775, 1052,   19,  664, 1349,  495, 2325,  602,  689,  942,  889,  740,  560,    0,  641,  547, 2641, 1035],  # 18 Santa Fe
    [  577, 1136, 1293,  601,  834,  586,  421,  642, 1293,  745, 1132, 1712,  915, 1088, 1382, 1316,  686,  412,  641,    0,  977, 2044,  477],  # 19 Santa Rosa
    [  401,  535,  629,  991,  311,  705, 1289,  566,  827, 1721,  521, 2677,  166,  141,  414,  353,  583,  643,  547,  977,    0, 3016, 1446],  # 20 Sgo. del Estero
    [ 2618, 3131, 3284, 2350, 2811, 2435, 1763, 2635, 3207, 1300, 3131, 1359, 2931, 3116, 3408, 3341, 2585, 2392, 2641, 2044, 3016,    0, 1605],  # 21 Ushuaia
    [ 1047, 1532, 1681,  789, 1311, 1019,  479, 1030, 1624,  327, 1526, 1294, 1391, 1562, 1855, 1790, 1141,  882, 1035,  477, 1446, 1605,    0],  # 22 Viedma
]

# Convertir a numpy array para comodidad
matriz_distancias = np.array(DISTANCIAS, dtype=float)


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def longitud_ruta(ruta):
    """Calcula la distancia total de una ruta circular."""
    distancia_total = 0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]
        distancia_total += matriz_distancias[ciudad_actual][ciudad_siguiente]
    return distancia_total


def graficar_ruta(ruta, titulo):
    """Grafica la ruta sobre un mapa esquemático de Argentina."""
    fig, ax = plt.subplots(figsize=(10, 14))

    # Dibujar contorno simplificado de Argentina
    contorno_lon = [
        -57.5, -55.0, -54.0, -55.5, -57.5, -58.5, -59.0, -58.0,
        -57.5, -57.0, -59.0, -62.0, -63.5, -65.5, -65.0, -64.0,
        -62.0, -62.5, -65.0, -67.0, -68.0, -69.5, -70.5, -71.5,
        -71.0, -70.0, -69.5, -69.0, -68.5, -68.0, -67.5, -66.0,
        -65.5, -64.5, -64.0, -62.0, -59.0, -57.5
    ]
    contorno_lat = [
        -22.0, -23.5, -25.5, -27.0, -29.0, -30.0, -32.0, -34.0,
        -35.5, -36.5, -38.0, -39.0, -40.0, -41.0, -42.5, -44.0,
        -45.0, -47.0, -49.0, -50.0, -51.0, -52.0, -53.0, -52.5,
        -50.0, -47.0, -44.0, -42.0, -40.0, -38.0, -35.0, -33.0,
        -30.0, -27.0, -25.0, -23.5, -23.0, -22.0
    ]
    ax.fill(contorno_lon, contorno_lat, color='#e8f5e9', alpha=0.5)
    ax.plot(contorno_lon, contorno_lat, color='#388e3c', linewidth=1.5, alpha=0.7)

    # Dibujar la ruta
    lons = [COORDENADAS[i][1] for i in ruta] + [COORDENADAS[ruta[0]][1]]
    lats = [COORDENADAS[i][0] for i in ruta] + [COORDENADAS[ruta[0]][0]]

    ax.plot(lons, lats, marker='o', linestyle='-', color='#1565c0',
            markersize=6, linewidth=1.8, zorder=3, label="Recorrido")
    ax.plot(lons[0], lats[0], marker='*', color='red', markersize=16,
            zorder=5, label=f"Inicio/Fin: {PROVINCIAS[ruta[0]]}")

    # Etiquetas de las ciudades
    for i in ruta:
        ax.annotate(PROVINCIAS[i],
                     (COORDENADAS[i][1], COORDENADAS[i][0]),
                     textcoords="offset points", xytext=(8, 4),
                     fontsize=7, color='#212121')

    dist = longitud_ruta(ruta)
    ax.set_title(f"{titulo}\nDistancia Total: {dist:.2f} km", fontsize=12, fontweight='bold')
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.legend(loc='lower left', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()



# =============================================================================
# EJERCICIO 2a – HEURÍSTICA VECINO MÁS CERCANO
# =============================================================================

def vecino_mas_cercano(inicio):
    """Desde la ciudad 'inicio', ir siempre a la ciudad más cercana
    no visitada. Devuelve la ruta como lista de índices."""
    visitadas = [inicio]
    actual = inicio
    ciudades_restantes = set(range(NUM_CIUDADES)) - {inicio}

    while ciudades_restantes:
        siguiente = min(ciudades_restantes,
                        key=lambda x: matriz_distancias[actual][x])
        visitadas.append(siguiente)
        ciudades_restantes.remove(siguiente)
        actual = siguiente

    return visitadas


# =============================================================================
# EJERCICIO 2c – ALGORITMO GENÉTICO
# =============================================================================

def cyclic_crossover(p1, p2):
    """Crossover cíclico (CX): crea dos hijos a partir de dos padres."""
    n = len(p1)
    c1 = [-1] * n
    c2 = [-1] * n

    ciclos = []
    visitados = set()

    idx = 0
    while len(visitados) < n:
        if idx in visitados:
            idx = next(i for i in range(n) if i not in visitados)

        ciclo = []
        inicio = idx
        while True:
            ciclo.append(idx)
            visitados.add(idx)
            val = p2[idx]
            idx = p1.index(val)
            if idx == inicio:
                break
        ciclos.append(ciclo)

    for num_ciclo, ciclo in enumerate(ciclos):
        if num_ciclo % 2 == 0:
            for pos in ciclo:
                c1[pos] = p1[pos]
                c2[pos] = p2[pos]
        else:
            for pos in ciclo:
                c1[pos] = p2[pos]
                c2[pos] = p1[pos]

    return c1, c2


def mutacion(individuo, tasa_mutacion=0.1):
    """Mutación por intercambio (swap) de dos genes."""
    if random.random() < tasa_mutacion:
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo


def algoritmo_genetico(N=50, M=200, tasa_crossover=0.8, tasa_mutacion=0.1):
    """
    Algoritmo genético para el TSP.

    Parámetros
    ----------
    N : int   – Número de cromosomas (tamaño de la población).
    M : int   – Cantidad de ciclos (generaciones).
    tasa_crossover : float – Probabilidad de aplicar crossover cíclico.
    tasa_mutacion  : float – Probabilidad de mutación (swap).

    Retorna
    -------
    mejor_ruta_global : list – La mejor ruta encontrada.
    """
    # Población inicial: permutaciones aleatorias
    poblacion = [random.sample(range(NUM_CIUDADES), NUM_CIUDADES)
                 for _ in range(N)]

    mejor_ruta_global = None
    mejor_distancia_global = float('inf')

    for _ciclo in range(M):
        # Evaluar fitness (1 / distancia)
        distancias = [longitud_ruta(ind) for ind in poblacion]

        for ind, dist in zip(poblacion, distancias):
            if dist < mejor_distancia_global:
                mejor_distancia_global = dist
                mejor_ruta_global = ind.copy()

        fitness = [1.0 / d for d in distancias]
        total_fitness = sum(fitness)
        probs = [f / total_fitness for f in fitness]

        # --- Selección y reproducción ---
        nueva_poblacion = []

        # Elitismo: mantener al mejor individuo
        mejor_idx = distancias.index(min(distancias))
        nueva_poblacion.append(poblacion[mejor_idx].copy())

        while len(nueva_poblacion) < N:
            # Selección por ruleta
            p1 = poblacion[np.random.choice(N, p=probs)]
            p2 = poblacion[np.random.choice(N, p=probs)]

            # Crossover cíclico (con probabilidad tasa_crossover)
            if random.random() < tasa_crossover:
                hijo1, hijo2 = cyclic_crossover(p1, p2)
            else:
                hijo1 = list(p1)
                hijo2 = list(p2)

            # Mutación
            hijo1 = mutacion(hijo1, tasa_mutacion)
            hijo2 = mutacion(hijo2, tasa_mutacion)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < N:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    return mejor_ruta_global


# =============================================================================
# MENÚ INTERACTIVO
# =============================================================================

def imprimir_ruta(ruta):
    """Imprime la ruta completa con nombres y regreso a la ciudad de partida."""
    recorrido = " -> ".join(PROVINCIAS[i] for i in ruta)
    recorrido += f" -> {PROVINCIAS[ruta[0]]}"
    print(f"\n  Ciudad de partida : {PROVINCIAS[ruta[0]]}")
    print(f"  Recorrido completo: {recorrido}")
    print(f"  Longitud del trayecto: {longitud_ruta(ruta):.2f} km")


def menu():
    while True:
        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║   MENÚ – PROBLEMA DEL VIAJANTE (TSP) – ARGENTINA       ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print("║  a) Vecino más cercano desde una ciudad elegida         ║")
        print("║  b) Mejor recorrido global (vecino más cercano)         ║")
        print("║  c) Algoritmo Genético (N=50, M=200, CX cíclico)       ║")
        print("║  d) Salir                                               ║")
        print("╚══════════════════════════════════════════════════════════╝")

        opcion = input("  Seleccione una opción: ").strip().lower()

        # ── Opción A ──────────────────────────────────────────────────
        if opcion == 'a':
            print("\n  Capitales disponibles:")
            for i in range(NUM_CIUDADES):
                print(f"    {i + 1:>2}. {PROVINCIAS[i]}")
            try:
                num = int(input("\n  Ingrese el número de la capital de partida (1-23): "))
                inicio = num - 1
                if 0 <= inicio < NUM_CIUDADES:
                    ruta = vecino_mas_cercano(inicio)
                    imprimir_ruta(ruta)
                    graficar_ruta(ruta,
                                 f"Heurística Vecino Más Cercano\n"
                                 f"(Inicio: {PROVINCIAS[inicio]})")
                else:
                    print("  Número fuera de rango.")
            except ValueError:
                print("  Entrada inválida.")

        # ── Opción B ──────────────────────────────────────────────────
        elif opcion == 'b':
            print("\n  Buscando el recorrido mínimo probando cada ciudad como inicio...")
            mejor_ruta = None
            mejor_distancia = float('inf')

            for i in range(NUM_CIUDADES):
                ruta = vecino_mas_cercano(i)
                dist = longitud_ruta(ruta)
                if dist < mejor_distancia:
                    mejor_distancia = dist
                    mejor_ruta = ruta

            print("\n  ═══ MEJOR RECORRIDO GLOBAL (Vecino Más Cercano) ═══")
            imprimir_ruta(mejor_ruta)
            graficar_ruta(mejor_ruta, "Mejor Ruta Global – Vecino Más Cercano")

        # ── Opción C ──────────────────────────────────────────────────
        elif opcion == 'c':
            print("\n  Ejecutando Algoritmo Genético...")
            print("    N (población)    = 50")
            print("    M (generaciones) = 200")
            print("    Crossover cíclico, tasa = 0.8")
            print("    Mutación (swap),  tasa = 0.1")
            print()

            ruta_ga = algoritmo_genetico(N=50, M=200,
                                         tasa_crossover=0.8,
                                         tasa_mutacion=0.1)
            print("  ═══ RESULTADO ALGORITMO GENÉTICO ═══")
            imprimir_ruta(ruta_ga)
            graficar_ruta(ruta_ga,
                          "Algoritmo Genético (N=50, M=200, CX Cíclico)")

        # ── Opción D ──────────────────────────────────────────────────
        elif opcion == 'd':
            print("\n  Saliendo del programa...")
            break
        else:
            print("  Opción no válida. Intente nuevamente.")


# =============================================================================
if __name__ == "__main__":
    menu()
