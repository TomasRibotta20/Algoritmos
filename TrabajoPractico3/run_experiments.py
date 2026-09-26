"""
Script auxiliar para ejecutar las comparaciones entre
Heurística (Vecino Más Cercano) y Algoritmo Genético.
Útil para generar datos para el informe.
"""

import tsp_argentina as tsp

# ─────────────────────────────────────────────────────────────────
# 1. VECINO MÁS CERCANO – Desde cada ciudad
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("  VECINO MÁS CERCANO – Resultados por ciudad de inicio")
print("=" * 60)

resultados_heur = []
for i in range(tsp.NUM_CIUDADES):
    ruta = tsp.vecino_mas_cercano(i)
    dist = tsp.longitud_ruta(ruta)
    resultados_heur.append((i, dist, ruta))
    print(f"  Inicio: {tsp.PROVINCIAS[i]:.<25s} Distancia: {dist:>10.2f} km")

# Mejor resultado global
mejor = min(resultados_heur, key=lambda x: x[1])
print(f"\n  - Mejor inicio: {tsp.PROVINCIAS[mejor[0]]}  ->  {mejor[1]:.2f} km")
print(f"  Recorrido: {' -> '.join(tsp.PROVINCIAS[c] for c in mejor[2])} -> {tsp.PROVINCIAS[mejor[2][0]]}")

# ─────────────────────────────────────────────────────────────────
# 2. ALGORITMO GENÉTICO – 10 ejecuciones
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ALGORITMO GENÉTICO – 10 ejecuciones (N=50, M=200)")
print("=" * 60)

resultados_ga = []
mejor_ga_dist = float('inf')
mejor_ga_ruta = None

for run in range(1, 11):
    ruta_ga = tsp.algoritmo_genetico(N=50, M=200,
                                      tasa_crossover=0.8,
                                      tasa_mutacion=0.1)
    dist_ga = tsp.longitud_ruta(ruta_ga)
    resultados_ga.append(dist_ga)
    if dist_ga < mejor_ga_dist:
        mejor_ga_dist = dist_ga
        mejor_ga_ruta = ruta_ga
    print(f"  Ejecución {run:>2d}:  {dist_ga:>10.2f} km")

promedio_ga = sum(resultados_ga) / len(resultados_ga)
print(f"\n  - Mejor GA:    {mejor_ga_dist:.2f} km")
print(f"  - Promedio GA: {promedio_ga:.2f} km")
print(f"  - Peor GA:     {max(resultados_ga):.2f} km")
print(f"  Mejor recorrido GA: {' -> '.join(tsp.PROVINCIAS[c] for c in mejor_ga_ruta)} -> {tsp.PROVINCIAS[mejor_ga_ruta[0]]}")

# ─────────────────────────────────────────────────────────────────
# 3. COMPARACIÓN
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  COMPARACIÓN: HEURÍSTICA vs ALGORITMO GENÉTICO")
print("=" * 60)
print(f"  Mejor Vecino Más Cercano:  {mejor[1]:>10.2f} km")
print(f"  Mejor Algoritmo Genético:  {mejor_ga_dist:>10.2f} km")
print(f"  Promedio AG (10 runs):     {promedio_ga:>10.2f} km")

diff = mejor[1] - mejor_ga_dist
if diff > 0:
    print(f"\n  El AG mejoró la heurística en {diff:.2f} km ({diff/mejor[1]*100:.1f}%)")
else:
    print(f"\n  La heurística fue mejor por {-diff:.2f} km ({-diff/mejor_ga_dist*100:.1f}%)")
