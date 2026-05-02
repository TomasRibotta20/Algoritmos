import motor_ag as ag
import random
import matplotlib.pyplot as plt

def obtener_padre_ruleta(poblacion, fitness_relativo):
    # 1. Crear el vector de 100 lugares
    ruleta_vector = []
    
    # Calculamos cuántos lugares le toca a cada uno
    casilleros_por_ind = []
    for f in fitness_relativo:
        lugares = int(f * 100)
        # Validación: si tiene algo de fitness, al menos 1 lugar
        if f > 0 and lugares == 0:
            lugares = 1
        casilleros_por_ind.append(lugares)
    
    # 2. Ajustar para que no sumen 101 ni 99 por redondeo
    while sum(casilleros_por_ind) != 100:
        index_max = casilleros_por_ind.index(max(casilleros_por_ind))
        if sum(casilleros_por_ind) > 100:
            casilleros_por_ind[index_max] -= 1
        else:
            casilleros_por_ind[index_max] += 1
            
    # 3. Llenar el vector con los índices de los individuos
    for i in range(len(casilleros_por_ind)):
        for _ in range(casilleros_por_ind[i]):
            ruleta_vector.append(i)
            
    # 4. Tirar el número aleatorio y ver dónde cayó
    tiro = random.randint(0, 99)
    indice_ganador = ruleta_vector[tiro]
    return poblacion[indice_ganador]

def ejecutar_opcion_a(generaciones):
    poblacion = ag.crear_poblacion()
    # Listas para el gráfico final
    max_history, min_history, prom_history, desv_history = [], [], [], []

    for g in range(generaciones):
        # f(x) de cada uno
        valores_decimales = [ag.binario_a_decimal(ind) for ind in poblacion]
        f_objetivo = [ag.funcion_objetivo(d) for d in valores_decimales]
        suma_f = sum(f_objetivo)
        
        # Fitness relativo (porcentaje)
        fitness = [f / suma_f if suma_f > 0 else 1/ag.POBLACION_TAM for f in f_objetivo]
        
        # Estadísticas para el cuadro
        mejor_f = max(f_objetivo)
        peor_f = min(f_objetivo)
        prom_f = suma_f / ag.POBLACION_TAM
        desv_fit = ag.calcular_desviacion_estandar(fitness)
        mejor_crom = "".join(map(str, poblacion[f_objetivo.index(mejor_f)]))
        
        print(f"Gen {g+1} | Máx Obj: {mejor_f:.4f} | Min Obj: {peor_f:.4f} | Desv Fit: {desv_fit:.4f}")
        print(f"Mejor Cromosoma: {mejor_crom}\n")

        # Guardar para gráfico
        max_history.append(mejor_f)
        min_history.append(peor_f)
        prom_history.append(prom_f)
        desv_history.append(desv_fit)

        # Reproducción
        nueva_pob = []
        while len(nueva_pob) < ag.POBLACION_TAM:
            p1 = obtener_padre_ruleta(poblacion, fitness)
            p2 = obtener_padre_ruleta(poblacion, fitness)
            h1, h2 = ag.cruce_un_punto(p1, p2)
            nueva_pob.append(ag.mutar_individuo(h1))
            if len(nueva_pob) < ag.POBLACION_TAM:
                nueva_pob.append(ag.mutar_individuo(h2))
        poblacion = nueva_pob

    # Gráfico Resumen
    plt.plot(max_history, label="Máximo Obj")
    plt.plot(min_history, label="Mínimo Obj")
    plt.plot(prom_history, label="Promedio Obj")
    plt.plot(desv_history, label="Desv. Est. Fitness")
    plt.legend()
    plt.title("Evolución Opcion A - Ruleta Rústica")
    plt.show()

if __name__ == "__main__":
    ejecutar_opcion_a(100)