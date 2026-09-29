import itertools
import math

def busqueda_exhaustiva(indices_ciudades, matriz, ciudad_inicio):
    otras_ciudades = [i for i in indices_ciudades if i != ciudad_inicio]
    mejor_recorrido = None
    mejor_distancia = float("inf")

    for permutacion in itertools.permutations(otras_ciudades):
        recorrido = [ciudad_inicio] + list(permutacion)
        distancia = 0
        for i in range(len(recorrido)):
            actual = recorrido[i]
            siguiente = recorrido[(i + 1) % len(recorrido)]
            distancia += matriz[actual][siguiente]
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_recorrido = recorrido

    return mejor_recorrido, mejor_distancia

def demo_reducida(matriz, cantidad=8):
    indices = list(range(cantidad))
    return busqueda_exhaustiva(indices, matriz, indices[0])

def calcular_cantidad_permutaciones(n):
    return math.factorial(n - 1) // 2

def estimar_tiempo_exhaustivo(n, permutaciones_por_segundo=2_000_000):
    cantidad = calcular_cantidad_permutaciones(n)
    segundos = cantidad / permutaciones_por_segundo
    return cantidad, segundos

def formatear_tiempo(segundos):
    anios = segundos / (60 * 60 * 24 * 365)
    if anios > 1:
        return f"{anios:.2e} años"
    dias = segundos / (60 * 60 * 24)
    if dias > 1:
        return f"{dias:.2f} días"
    horas = segundos / 3600
    if horas > 1:
        return f"{horas:.2f} horas"
    return f"{segundos:.2f} segundos"

def justificacion_teorica(n=23):
    cantidad, segundos = estimar_tiempo_exhaustivo(n)
    print(f"Fijando la ciudad de partida, la cantidad de recorridos distintos posibles")
    print(f"para {n} ciudades es (n-1)!/2 (se divide por 2 porque un recorrido y su")
    print(f"inverso recorren la misma distancia total).")
    print(f"\n({n}-1)! / 2 = {cantidad:,} recorridos a evaluar.")
    print(f"\nEvaluando {2_000_000:,} recorridos por segundo, el método exhaustivo")
    print(f"tardaría aproximadamente {formatear_tiempo(segundos)}.")
    print(f"\nConclusión: el método exhaustivo es computacionalmente intratable para")
    print(f"las {n} capitales (crecimiento factorial), por lo que se debe recurrir a")
    print(f"heurísticas o metaheurísticas como el algoritmo genético.")
