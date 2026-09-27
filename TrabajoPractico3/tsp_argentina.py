import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os
import time
import geopandas as gpd
import math
import csv

# =============================================================================
# TRABAJO PRÁCTICO N°3 - PROBLEMA DEL VIAJANTE (TSP)
# Capitales de provincias de la República Argentina
# =============================================================================

# 23 capitales provinciales (sin CABA)
# Índice 0..22 (internamente)
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
NUM_CIUDADES = len(PROVINCIAS) # 23

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

def cargar_matriz_desde_csv(ruta_archivo):
    try:
        df = pd.read_csv(ruta_archivo)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró '{ruta_archivo}'.")
    except Exception:
        raise ValueError(f"'{ruta_archivo}' no pudo leerse como CSV.")
    try:
        df = df.iloc[1:24, :]
        df = df.drop(columns=df.columns[0])
        df = df.drop(columns=df.columns[0])
        df = df.fillna(0)
        matriz = df.to_numpy(dtype=float)
    except Exception:
        raise ValueError("El CSV no tiene el formato esperado (24 filas × 25 columnas).")

    if matriz.shape != (23, 23):
        raise ValueError(f"Se esperaba 23×23 pero se obtuvo {matriz.shape}.")
    return matriz
    
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(DIRECTORIO_ACTUAL, "distancias.csv")

matriz_distancias = cargar_matriz_desde_csv(ARCHIVO_CSV)

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
    fix, ax = plt.subplots(figsize=(10, 14))
    ruta_mapa = os.path.join(DIRECTORIO_ACTUAL, "datos_mapa", "ne_110m_admin_0_countries.shp")
    mundo = gpd.read_file(ruta_mapa)
    argentina = mundo[mundo["NAME"] == "Argentina"]
    argentina.plot(ax=ax, color="#e8f5e9", edgecolor="#388e3c")

    lons = [COORDENADAS[i][1] for i in ruta] + [COORDENADAS[ruta[0]][1]]
    lats = [COORDENADAS[i][0] for i in ruta] + [COORDENADAS[ruta[0]][0]]

    ax.plot(lons, lats, marker='o', linestyle='-', color='#1565c0',
            markersize=6, linewidth=1.8, zorder=3, label="Recorrido")
    ax.plot(lons[0], lats[0], marker='*', color='red', markersize=16,
            zorder=5, label=f"Inicio/Fin: {PROVINCIAS[ruta[0]]}")
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
# EJERCICIO 1 – Método exhaustivo
# =============================================================================

def _generar_rutas(ciudades_restantes, ruta_actual, todas_las_rutas):
    """Función auxiliar recursiva que genera todas las permutaciones."""
    if not ciudades_restantes:
        todas_las_rutas.append(ruta_actual[:])
        return
    for i, ciudad in enumerate(ciudades_restantes):
        ruta_actual.append(ciudad)
        _generar_rutas(
            ciudades_restantes[:i] + ciudades_restantes[i+1:],
            ruta_actual,
            todas_las_rutas
        )
        ruta_actual.pop()


def busqueda_exhaustiva(n_ciudades):
    """Genera todas las rutas posibles y devuelve la mejor."""
    todas_las_rutas = []
    _generar_rutas(list(range(1, n_ciudades)), [0], todas_las_rutas)

    mejor_ruta = None
    mejor_dist = float('inf')
    for ruta in todas_las_rutas:
        dist = longitud_ruta(ruta)
        if dist < mejor_dist:
            mejor_dist = dist
            mejor_ruta = ruta

    return mejor_ruta, mejor_dist, len(todas_las_rutas)


def demostrar_inviabilidad():
    """Ejecuta el exhaustivo para N creciente"""
    
    print("=" * 60)
    print("  BÚSQUEDA EXHAUSTIVA – Análisis de viabilidad")
    print("=" * 60)
    print(f"  {'N':>4}  {'Rutas':>12}  {'Tiempo':>12}")
    print(f"  {'-'*4}  {'-'*12}  {'-'*12}")

    ultimo_tiempo = None
    ultimo_n = None
    resultados = []
    for n in range(5, 12):
        inicio = time.time()
        _, _, total_rutas = busqueda_exhaustiva(n)
        tiempo = time.time() - inicio

        print(f"  {n:>4}  {total_rutas:>12,}  {tiempo:>11.4f}s")
        
        resultados.append((n, total_rutas, tiempo))
        ultimo_tiempo = tiempo
        ultimo_n = n

    # Extrapolación: de ultimo_n a 23
    # La diferencia en rutas es (22! / (ultimo_n - 1)!)
    factor = math.factorial(22) // math.factorial(ultimo_n - 1)
    tiempo_estimado_s = ultimo_tiempo * factor
    tiempo_estimado_años = tiempo_estimado_s / (60 * 60 * 24 * 365)
    print(f"\n  Rutas para N=23:  {math.factorial(22):,}")
    print(f"  Tiempo estimado:  {tiempo_estimado_años:.2e} años")
    print(f"\n  Conclusión: el método exhaustivo es computacionalmente")
    print(f"  inviable para 23 ciudades. Se requieren heurísticas.")
    print("=" * 60)

    return resultados

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
# EJERCICIO 2b – Mejor recorrido global
# =============================================================================

def mejor_ruta_global():
    """Prueba todas las ciudades como inicio y devuelve la mejor ruta."""
    mejor_ruta = None
    mejor_distancia = float('inf')
    resultados = []
    for i in range(NUM_CIUDADES):
        ruta = vecino_mas_cercano(i)
        dist = longitud_ruta(ruta)
        resultados.append((PROVINCIAS[i], dist))
        if dist < mejor_distancia:
            mejor_distancia = dist
            mejor_ruta = ruta

    return mejor_ruta, mejor_distancia, resultados  

# =============================================================================
# EJERCICIO 2c – ALGORITMO GENÉTICO
# =============================================================================

def construir_ruleta(probs):
    casilleros = [max(1, int(f * 100)) for f in probs]
    
    while sum(casilleros) != 100:
        idx = casilleros.index(max(casilleros))
        casilleros[idx] += 1 if sum(casilleros) < 100 else -1
    ruleta_vector = []
    
    for i, cant in enumerate(casilleros):
        ruleta_vector.extend([i] * cant)

    return ruleta_vector


def obtener_padre_ruleta(poblacion, ruleta_vector):
    idx = ruleta_vector[random.randint(0, 99)]
    return poblacion[idx]


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
    """Mutación por intercambio de dos genes."""
    if random.random() < tasa_mutacion:
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo


def algoritmo_genetico(N=50, M=200, tasa_crossover=0.8, tasa_mutacion=0.1):
    """Algoritmo genético para el TSP.

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
    poblacion = [random.sample(range(NUM_CIUDADES), NUM_CIUDADES)
                 for _ in range(N)]

    mejor_ruta_global = None
    mejor_distancia_global = float('inf')
    historial = []

    for _ciclo in range(M):
        distancias = [longitud_ruta(ind) for ind in poblacion]

        for ind, dist in zip(poblacion, distancias):
            if dist < mejor_distancia_global:
                mejor_distancia_global = dist
                mejor_ruta_global = ind.copy()

        historial.append((_ciclo + 1, mejor_distancia_global))

        fitness = [1.0 / d for d in distancias]
        total_fitness = sum(fitness)
        probs = [f / total_fitness for f in fitness]

        nueva_poblacion = []

        mejor_idx = distancias.index(min(distancias))
        nueva_poblacion.append(poblacion[mejor_idx].copy())

        while len(nueva_poblacion) < N:
            ruleta_vector = construir_ruleta(probs)
            p1 = obtener_padre_ruleta(poblacion, ruleta_vector)
            p2 = obtener_padre_ruleta(poblacion, ruleta_vector)

            if random.random() < tasa_crossover:
                hijo1, hijo2 = cyclic_crossover(p1, p2)
            else:
                hijo1 = list(p1)
                hijo2 = list(p2)
            hijo1 = mutacion(hijo1, tasa_mutacion)
            hijo2 = mutacion(hijo2, tasa_mutacion)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < N:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    return mejor_ruta_global, historial


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
        print("\n|----------------------------------------------------------|")
        print("|   MENÚ – PROBLEMA DEL VIAJANTE (TSP) – ARGENTINA         |")
        print("|----------------------------------------------------------|")
        print("|  1) Ejercicio 1 – Método Exhaustivo (Justificación)      |")
        print("|  2) Ejercicio 2a – Vecino más cercano desde una ciudad   |")
        print("|  3) Ejercicio 2b – Mejor recorrido global (heurística)   |")
        print("|  4) Ejercicio 2c  – Algoritmo Genético (N=50, M=200)     |")
        print("|  0) Salir                                                |")
        print("|----------------------------------------------------------|")

        opcion = input("  Seleccione una opción: ").strip().lower()

        # Ejercicio 1 --------------------------------------------------
        if opcion == '1':
            resultados = demostrar_inviabilidad()

            # ====== Exporta a CSV =====================================
            with open("exhaustivo.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["N", "Rutas", "Tiempo (s)"])
                for n, rutas, tiempo in resultados:
                    writer.writerow([n, rutas, f"{tiempo:.6f}"])
                writer.writerow([23, math.factorial(22), "estimado"])
            print("  Exportado a exhaustivo.csv")
            # ==========================================================

        # Ejercicio 2a --------------------------------------------------
        elif opcion == '2':
            print("\n  Capitales disponibles:")
            for i in range(NUM_CIUDADES):
                print(f"    {i + 1:>2}. {PROVINCIAS[i]}")
            try:
                num = int(input("\n  Ingrese el número de la capital de partida (1-23): "))
                inicio = num - 1
                if 0 <= inicio < NUM_CIUDADES:
                    ruta = vecino_mas_cercano(inicio)
                    imprimir_ruta(ruta)
                    graficar_ruta(ruta, f"Heurística Vecino Más Cercano\n" f"(Inicio: {PROVINCIAS[inicio]})")

                    # ====== Exporta a CSV =====================================
                    acumulada = 0
                    with open("heuristica_2a.csv", "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(["Orden", "Ciudad", "Distancia Acumulada (km)"])
                        writer.writerow([1, PROVINCIAS[ruta[0]], f"{acumulada:.2f}"])
                        for i in range(1, len(ruta)):
                            acumulada += matriz_distancias[ruta[i-1]][ruta[i]]
                            writer.writerow([i+1, PROVINCIAS[ruta[i]], f"{acumulada:.2f}"])
                        acumulada += matriz_distancias[ruta[-1]][ruta[0]]
                        writer.writerow(["Regreso", PROVINCIAS[ruta[0]], f"{acumulada:.2f}"])
                    print("  Exportado a heuristica_2a.csv")
                    # ==========================================================
                else:
                    print("  Número fuera de rango.")
            except ValueError:
                print("  Entrada inválida.")

        # Ejercicio 2b --------------------------------------------------
        elif opcion == '3':
            print("\n  Buscando el recorrido mínimo probando cada ciudad como inicio...")
            mejor_ruta, mejor_distancia, resultados = mejor_ruta_global()
            print("\n  --- MEJOR RECORRIDO GLOBAL (Vecino Más Cercano) ---")
            imprimir_ruta(mejor_ruta)
            graficar_ruta(mejor_ruta, "Mejor Ruta Global – Vecino Más Cercano")

            # ====== Exporta a CSV =====================================
            with open("heuristica_2b.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                writer.writerow(["Ciudad Inicio", "Distancia Total (km)"])
                for ciudad, dist in resultados:
                    writer.writerow([ciudad, f"{dist:.2f}"])
                writer.writerow(["MEJOR", f"{mejor_distancia:.2f}"])
                
                writer.writerow([])
                writer.writerow(["--- RECORRIDO DE LA MEJOR RUTA ---"])
                
                writer.writerow(["Orden", "Ciudad", "Distancia Acumulada (km)"])
                acumulada = 0
                writer.writerow([1, PROVINCIAS[mejor_ruta[0]], f"{acumulada:.2f}"])
                for i in range(1, len(mejor_ruta)):
                    acumulada += matriz_distancias[mejor_ruta[i-1]][mejor_ruta[i]]
                    writer.writerow([i+1, PROVINCIAS[mejor_ruta[i]], f"{acumulada:.2f}"])
                acumulada += matriz_distancias[mejor_ruta[-1]][mejor_ruta[0]]
                writer.writerow(["Regreso", PROVINCIAS[mejor_ruta[0]], f"{acumulada:.2f}"])
            print("  Exportado a heuristica_2b.csv")
            # ==========================================================
        # Ejercicio 2c  --------------------------------------------------
        elif opcion == '4':
            print("\n  Ejecutando Algoritmo Genético...")
            print("    N (población)    = 50")
            print("    M (generaciones) = 200")
            print("    Crossover cíclico, tasa = 0.8")
            print("    Mutación (swap),  tasa = 0.1")
            print()
            
            ruta_ga, historial_ga = algoritmo_genetico(N=50, M=200, tasa_crossover=0.8, tasa_mutacion=0.1)
            
            print("  --- RESULTADO ALGORITMO GENÉTICO ---")
            imprimir_ruta(ruta_ga)
            graficar_ruta(ruta_ga, "Algoritmo Genético (N=50, M=200, CX Cíclico)")

            # ====== Exporta a CSV =====================================
            with open("genetico.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Generación", "Mejor Distancia (km)"])
                for gen, dist in historial_ga:
                    writer.writerow([gen, f"{dist:.2f}"])
            print("  Exportado a genetico.csv")
            # ==========================================================
        # Salir --------------------------------------------------
        elif opcion == '0':
            print("\n  Saliendo del programa...")
            break
        else:
            print("  Opción no válida. Intente nuevamente.")

# =============================================================================
if __name__ == "__main__":
    menu()