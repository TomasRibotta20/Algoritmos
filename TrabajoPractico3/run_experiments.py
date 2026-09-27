import tsp_argentina as tsp
import csv
import time

# =============================================================================
# 1. VECINO MÁS CERCANO – Desde cada ciudad
# =============================================================================
print("=" * 60)
print("  VECINO MÁS CERCANO – Resultados por ciudad de inicio")
print("=" * 60)

resultados_heur = []
inicio_heur = time.time()
for i in range(tsp.NUM_CIUDADES):
    ruta = tsp.vecino_mas_cercano(i)
    dist = tsp.longitud_ruta(ruta)
    resultados_heur.append((i, dist, ruta))
    print(f"  Inicio: {tsp.PROVINCIAS[i]:.<25s} Distancia: {dist:>10.2f} km")
tiempo_heur = time.time() - inicio_heur
print(f"\n  Tiempo total heurística: {tiempo_heur:.4f} seg")

mejor = min(resultados_heur, key=lambda x: x[1])
print(f"\n  - Mejor inicio: {tsp.PROVINCIAS[mejor[0]]}  ->  {mejor[1]:.2f} km")
print(f"  Recorrido: {' -> '.join(tsp.PROVINCIAS[c] for c in mejor[2])} -> {tsp.PROVINCIAS[mejor[2][0]]}")

# =============================================================================
# 2. ALGORITMO GENÉTICO – 10 ejecuciones
# =============================================================================
print("\n" + "=" * 60)
print("  ALGORITMO GENÉTICO – 10 ejecuciones (N=50, M=200)")
print("=" * 60)

resultados_ga = []
mejor_ga_dist = float('inf')
mejor_ga_ruta = None

inicio_ga = time.time()
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
tiempo_ga = time.time() - inicio_ga
print(f"\n  Tiempo total AG (10 runs): {tiempo_ga:.4f} seg")
print(f"  Tiempo promedio por run:   {tiempo_ga/10:.4f} seg")
promedio_ga = sum(resultados_ga) / len(resultados_ga)
print(f"\n  - Mejor GA:    {mejor_ga_dist:.2f} km")
print(f"  - Promedio GA: {promedio_ga:.2f} km")
print(f"  - Peor GA:     {max(resultados_ga):.2f} km")
print(f"  Mejor recorrido GA: {' -> '.join(tsp.PROVINCIAS[c] for c in mejor_ga_ruta)} -> {tsp.PROVINCIAS[mejor_ga_ruta[0]]}")

# =============================================================================
# 3. COMPARACIÓN
# =============================================================================
print("\n" + "=" * 60)
print("  COMPARACIÓN: HEURÍSTICA vs ALGORITMO GENÉTICO")
print("=" * 60)
print(f"  Mejor Vecino Más Cercano:  {mejor[1]:>10.2f} km")
print(f"  Mejor Algoritmo Genético:  {mejor_ga_dist:>10.2f} km")
print(f"  Promedio AG (10 corridas):     {promedio_ga:>10.2f} km")

diff = mejor[1] - mejor_ga_dist
if diff > 0:
    print(f"\n  El AG mejoró la heurística en {diff:.2f} km ({diff/mejor[1]*100:.1f}%)")
else:
    print(f"\n  La heurística fue mejor por {-diff:.2f} km ({-diff/mejor_ga_dist*100:.1f}%)")
print(f"  Tiempo Heurística: {tiempo_heur:.4f} seg")
print(f"  Tiempo AG (prom):  {tiempo_ga/10:.4f} seg")

# =============================================================================
# 4. EXPORTAR A CSV
# =============================================================================
with open("resultados_comparacion.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Método", "Ciudad Inicio", "Distancia (km)"])
    
    for i, dist, _ in resultados_heur:
        writer.writerow(["Heurística", tsp.PROVINCIAS[i], f"{dist:.2f}"])
    
    for run, dist in enumerate(resultados_ga, 1):
        writer.writerow([f"AG Run {run}", "-", f"{dist:.2f}"])

print("\n  Resultados exportados a resultados_comparacion.csv")