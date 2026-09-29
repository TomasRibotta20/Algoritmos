import random

POBLACION_TAM = 50
GENERACIONES = 200
PROB_CROSSOVER = 0.85
PROB_MUTACION = 0.15
PORCENTAJE_ELITE = 0.1
TAM_TORNEO = 5

def longitud_recorrido(recorrido, matriz):
    total = 0
    for i in range(len(recorrido)):
        actual = recorrido[i]
        siguiente = recorrido[(i + 1) % len(recorrido)]
        total += matriz[actual][siguiente]
    return total

def crear_individuo(cantidad_ciudades):
    individuo = list(range(cantidad_ciudades))
    random.shuffle(individuo)
    return individuo

def crear_poblacion(cantidad_ciudades):
    return [crear_individuo(cantidad_ciudades) for _ in range(POBLACION_TAM)]

def calcular_fitness(individuo, matriz):
    return 1 / longitud_recorrido(individuo, matriz)

def seleccion_torneo(poblacion, fitness):
    participantes = random.sample(range(len(poblacion)), TAM_TORNEO)
    ganador = participantes[0]
    for i in participantes:
        if fitness[i] > fitness[ganador]:
            ganador = i
    return poblacion[ganador][:]

def cruce_ciclico(padre1, padre2):
    n = len(padre1)
    ciclos = [0] * n
    ciclo_actual = 1

    while 0 in ciclos:
        indice = ciclos.index(0)
        valor_inicio = padre1[indice]
        while True:
            ciclos[indice] = ciclo_actual
            valor_buscado = padre2[indice]
            indice = padre1.index(valor_buscado)
            if padre1[indice] == valor_inicio:
                break
        ciclo_actual += 1

    hijo1 = [None] * n
    hijo2 = [None] * n
    for i in range(n):
        if ciclos[i] % 2 == 1:
            hijo1[i] = padre1[i]
            hijo2[i] = padre2[i]
        else:
            hijo1[i] = padre2[i]
            hijo2[i] = padre1[i]

    return hijo1, hijo2

def mutar_individuo(individuo):
    if random.random() < PROB_MUTACION:
        n = len(individuo)
        i, j = random.sample(range(n), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def obtener_elite(poblacion, fitness):
    cantidad = max(1, int(POBLACION_TAM * PORCENTAJE_ELITE))
    combinado = sorted(zip(poblacion, fitness), key=lambda x: x[1], reverse=True)
    return [individuo[:] for individuo, fit in combinado[:cantidad]]

def ejecutar_algoritmo_genetico(matriz, cantidad_ciudades):
    poblacion = crear_poblacion(cantidad_ciudades)
    historial = []
    mejor_global = None
    mejor_distancia_global = float("inf")

    for gen in range(GENERACIONES):
        distancias = [longitud_recorrido(ind, matriz) for ind in poblacion]
        fitness = [1 / d for d in distancias]

        idx_mejor = distancias.index(min(distancias))
        if distancias[idx_mejor] < mejor_distancia_global:
            mejor_distancia_global = distancias[idx_mejor]
            mejor_global = poblacion[idx_mejor][:]

        historial.append({
            "Gen": gen + 1,
            "Mejor": min(distancias),
            "Peor": max(distancias),
            "Promedio": sum(distancias) / len(distancias),
        })

        nueva_poblacion = obtener_elite(poblacion, fitness)

        while len(nueva_poblacion) < POBLACION_TAM:
            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)

            if random.random() < PROB_CROSSOVER:
                hijo1, hijo2 = cruce_ciclico(padre1, padre2)
            else:
                hijo1, hijo2 = padre1[:], padre2[:]

            hijo1 = mutar_individuo(hijo1)
            hijo2 = mutar_individuo(hijo2)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < POBLACION_TAM:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion[:POBLACION_TAM]

    return mejor_global, mejor_distancia_global, historial
