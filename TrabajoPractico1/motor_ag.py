import random

# Constantes
CANT_GENES = 30
POBLACION_TAM = 10
COEF = 2**30 - 1
PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05

def funcion_objetivo(valor_decimal):
    """Calcula f(x) = (x/coef)^2"""
    return (valor_decimal / COEF) ** 2

def binario_a_decimal(cromosoma):
    """Conversión manual de binario a decimal"""
    decimal = 0
    for i in range(len(cromosoma)):
        bit = cromosoma[i]
        potencia = (len(cromosoma) - 1) - i
        if bit == 1:
            decimal += 2 ** potencia
    return decimal

def calcular_desviacion_estandar(valores):
    """Cálculo manual de sigma"""
    n = len(valores)
    if n == 0: return 0
    promedio = sum(valores) / n
    suma_cuadrados = sum((x - promedio) ** 2 for x in valores)
    return (suma_cuadrados / n) ** 0.5

def cruce_un_punto(p1, p2):
    """Crossover manual"""
    if random.random() < PROB_CROSSOVER:
        punto = random.randint(1, CANT_GENES - 1)
        hijo1 = p1[:punto] + p2[punto:]
        hijo2 = p2[:punto] + p1[punto:]
        return hijo1, hijo2
    return p1[:], p2[:]

def mutar_individuo(cromosoma):
    """Mutación"""
    if random.random() < PROB_MUTACION:
        pos = random.randint(0, CANT_GENES - 1)
        cromosoma[pos] = 1 - cromosoma[pos]
    return cromosoma

def crear_poblacion():
    return [[random.randint(0, 1) for _ in range(CANT_GENES)] for _ in range(POBLACION_TAM)]