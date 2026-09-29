def vecino_mas_cercano(ciudad_inicio, matriz, cantidad_ciudades):
    visitadas = [False] * cantidad_ciudades
    recorrido = [ciudad_inicio]
    visitadas[ciudad_inicio] = True
    actual = ciudad_inicio

    for _ in range(cantidad_ciudades - 1):
        mas_cercana = None
        distancia_minima = float("inf")
        for j in range(cantidad_ciudades):
            if not visitadas[j] and matriz[actual][j] < distancia_minima:
                distancia_minima = matriz[actual][j]
                mas_cercana = j
        recorrido.append(mas_cercana)
        visitadas[mas_cercana] = True
        actual = mas_cercana

    return recorrido

def longitud_recorrido(recorrido, matriz):
    total = 0
    for i in range(len(recorrido)):
        actual = recorrido[i]
        siguiente = recorrido[(i + 1) % len(recorrido)]
        total += matriz[actual][siguiente]
    return total

def mejor_recorrido_todas_las_capitales(matriz, cantidad_ciudades):
    mejor_recorrido = None
    mejor_distancia = float("inf")
    mejor_inicio = None
    resultados = []

    for inicio in range(cantidad_ciudades):
        recorrido = vecino_mas_cercano(inicio, matriz, cantidad_ciudades)
        distancia = longitud_recorrido(recorrido, matriz)
        resultados.append((inicio, recorrido, distancia))
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_recorrido = recorrido
            mejor_inicio = inicio

    return mejor_inicio, mejor_recorrido, mejor_distancia, resultados
