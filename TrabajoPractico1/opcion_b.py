import motor_ag as ag
import random
import matplotlib.pyplot as plt
import pandas as pd

def seleccion_torneo_rustica(poblacion, fitness_relativo):
    # El tamaño del torneo es el 40% de la población 
    k = int(ag.POBLACION_TAM * 0.4)
    if k < 2: k = 2
    
    def elegir_un_padre():
        # 1. Seleccionar k aspirantes 
        indices_participantes = []
        while len(indices_participantes) < k:
            indice_azar = random.randint(0, ag.POBLACION_TAM - 1)
            # Evitamos repetir el mismo individuo en el mismo torneo
            if indice_azar not in indices_participantes:
                indices_participantes.append(indice_azar)
        
        # 2. El ganador es el que tiene mayor FITNESS
        indice_ganador = indices_participantes[0]
        for idx in indices_participantes:
            if fitness_relativo[idx] > fitness_relativo[indice_ganador]:
                indice_ganador = idx
        
        return poblacion[indice_ganador]

    # Retornamos los dos padres para el cruce
    return elegir_un_padre(), elegir_un_padre()

def ejecutar_opcion_b(generaciones):
    poblacion = ag.crear_poblacion()
    historial = []

    for g in range(generaciones):
        # Evaluación manual
        valores_decimales = [ag.binario_a_decimal(ind) for ind in poblacion]
        f_obj = [ag.funcion_objetivo(d) for d in valores_decimales]
        
        # Fitness relativo: f(x) / sum(f(x))
        suma_f = sum(f_obj)
        fitness = [valor / suma_f if suma_f > 0 else 1/ag.POBLACION_TAM for valor in f_obj]
        
        # Estadísticas de la generación
        mejor_f_obj = max(f_obj)
        indice_mejor = f_obj.index(mejor_f_obj)
        mejor_cromosoma = "".join(map(str, poblacion[indice_mejor]))
        desv_fitness = ag.calcular_desviacion_estandar(fitness)

        historial.append({
            'Generacion': g + 1,
            'Mejor_Cromosoma': mejor_cromosoma,
            'Max_Obj': mejor_f_obj,
            'Min_Obj': min(f_obj),
            'Promedio_Obj': suma_f / ag.POBLACION_TAM,
            'Desv_Fitness': desv_fitness
        })

        # Cuadro por consola
        print(f"Gen {g+1:3} | Torneo | Máx Obj: {mejor_f_obj:.6f} | Desv Fit: {desv_fitness:.6f}")

        # Nueva Generación
        nueva_pob = []
        while len(nueva_pob) < ag.POBLACION_TAM:
            p1, p2 = seleccion_torneo_rustica(poblacion, fitness)
            h1, h2 = ag.cruce_un_punto(p1, p2)
            nueva_pob.append(ag.mutar_individuo(h1))
            if len(nueva_pob) < ag.POBLACION_TAM:
                nueva_pob.append(ag.mutar_individuo(h2))
        poblacion = nueva_pob

    # Gráfico resumen
    df = pd.DataFrame(historial)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Max_Obj'], label='Máximo F. Objetivo')
    plt.plot(df['Promedio_Obj'], label='Promedio F. Objetivo', linestyle='--')
    plt.title(f"Opción B: Torneo Rústico (40%) - {generaciones} Gen")
    plt.legend()
    plt.grid(True)
    plt.show()
    return df

if __name__ == "__main__":
    ejecutar_opcion_b(200)