import math

RADIO_TIERRA_KM = 6371

def distancia_haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return RADIO_TIERRA_KM * c

def construir_matriz_distancias(ciudades):
    n = len(ciudades)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matriz[i][j] = distancia_haversine(
                    ciudades[i]["lat"], ciudades[i]["lon"],
                    ciudades[j]["lat"], ciudades[j]["lon"]
                )
    return matriz

def longitud_recorrido(recorrido, matriz):
    total = 0
    for i in range(len(recorrido)):
        actual = recorrido[i]
        siguiente = recorrido[(i + 1) % len(recorrido)]
        total += matriz[actual][siguiente]
    return total
