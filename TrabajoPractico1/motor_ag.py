import random
import matplotlib.pyplot as plt
import pandas as pd
import os

# Constantes del problema
CANT_GENES = 30
POBLACION_TAM = 10
COEF = 2**30 - 1
PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05

def funcion_objetivo(valor_decimal):
    return (valor_decimal / COEF) ** 2

def binario_a_decimal(cromosoma):
    decimal = 0
    for i in range(len(cromosoma)):
        bit = cromosoma[i]
        potencia = (len(cromosoma) - 1) - i
        if bit == 1:
            decimal += 2 ** potencia
    return decimal

def calcular_desviacion_estandar(valores):
    n = len(valores)
    if n == 0: return 0
    promedio = sum(valores) / n
    suma_cuadrados = sum((x - promedio) ** 2 for x in valores)
    return (suma_cuadrados / n) ** 0.5

def cruce_un_punto(p1, p2):
    if random.random() < PROB_CROSSOVER:
        punto = random.randint(1, CANT_GENES - 1)
        return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:]
    return p1[:], p2[:]

def mutar_individuo(cromosoma):
    if random.random() < PROB_MUTACION:
        pos = random.randint(0, CANT_GENES - 1)
        cromosoma[pos] = 1 - cromosoma[pos]
    return cromosoma

def crear_poblacion():
    return [[random.randint(0, 1) for _ in range(CANT_GENES)] for _ in range(POBLACION_TAM)]

def obtener_elite(poblacion, fitness):
    """Selecciona el 20% de los mejores basándose en FITNESS"""
    cantidad = max(2, int(POBLACION_TAM * 0.2))
    combinado = sorted(zip(poblacion, fitness), key=lambda x: x[1], reverse=True)
    return [c[0][:] for c in combinado[:cantidad]]

def graficar_y_guardar(historial, metodo, generaciones, elitismo, tiempo):
    """Gráfico estandarizado con parámetros del GA"""
    df = pd.DataFrame(historial)
    os.makedirs("graficos_resultados", exist_ok=True)
    
    plt.figure(figsize=(10, 7))
    plt.plot(df['Max'], label="Máximo Obj")
    plt.plot(df['Min'], label="Mínimo Obj")
    plt.plot(df['Prom'], label="Promedio Obj")
    plt.plot(df['Desv_Fit'], label="Desv. Est. Fitness", color='red')
    
    estado_elitismo = "Si" if elitismo else "No"
    params = f"Población: {POBLACION_TAM} | Pc: {PROB_CROSSOVER} | Pm: {PROB_MUTACION}"
    plt.title(f"Método: {metodo} | Gen: {generaciones} | Elitismo: {estado_elitismo} | Tiempo Compilacion: {tiempo:.4f} seg\n{params}")
    plt.xlabel("Generación"); plt.ylabel("Valor")
    plt.legend(); plt.grid(True)
    
    nombre_arch = f"{metodo}_{generaciones}gen_elitismo_{estado_elitismo}.png"
    plt.savefig(f"graficos_resultados/{nombre_arch}")
    plt.show()