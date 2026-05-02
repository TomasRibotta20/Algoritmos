import motor_ag as ag
import opcion_a as opt_a # Importamos para usar la ruleta rústica
import matplotlib.pyplot as plt
import pandas as pd

def obtener_elite_por_fitness(poblacion, fitness_relativo):
    """
    Selecciona el 20% de los mejores individuos basándose en el FITNESS.
    """
    # Calculamos la cantidad 
    cantidad_elite = int(ag.POBLACION_TAM * 0.2)
    if cantidad_elite < 1: cantidad_elite = 1
    
    # Creamos lista de tuplas (cromosoma, valor_fitness)
    combinado = []
    for i in range(len(poblacion)):
        combinado.append((poblacion[i], fitness_relativo[i]))
    
    # Ordenamos de mayor a menor fitness usando el sort de Python
    combinado.sort(key=lambda x: x[1], reverse=True)
    
    # Extraemos los mejores (haciendo copia [:] de los bits)
    elite = []
    for i in range(cantidad_elite):
        elite.append(combinado[i][0][:])
        
    return elite

def ejecutar_opcion_c(generaciones):
    poblacion = ag.crear_poblacion()
    historial = []

    for g in range(generaciones):
        # 1. Evaluación manual de la función objetivo para cada individuo
        valores_decimales = [ag.binario_a_decimal(ind) for ind in poblacion]
        f_objetivo = [ag.funcion_objetivo(d) for d in valores_decimales]
        
        # 2. Cálculo de Fitness 
        suma_f = sum(f_objetivo)
        fitness = [f / suma_f if suma_f > 0 else 1/ag.POBLACION_TAM for f in f_objetivo]
        
        # 3. Estadísticas de la generación (Función Objetivo y Desv. de Fitness)
        max_obj = max(f_objetivo)
        min_obj = min(f_objetivo)
        prom_obj = suma_f / ag.POBLACION_TAM
        desv_fit = ag.calcular_desviacion_estandar(fitness)
        
        # Identificar mejor cromosoma (el de mayor f_objetivo/fitness)
        indice_mejor = f_objetivo.index(max_obj)
        mejor_cromosoma = "".join(map(str, poblacion[indice_mejor]))
        
        historial.append({
            'Generacion': g + 1,
            'Mejor_Cromosoma': mejor_cromosoma,
            'Max_Obj': max_obj,
            'Min_Obj': min_obj,
            'Promedio_Obj': prom_obj,
            'Desv_Fitness': desv_fit
        })

        # Cuadro por consola
        print(f"Gen {g+1:3} | Elitismo (Fitness) | Máx Obj: {max_obj:.6f} | Desv Fit: {desv_fit:.6f}")
        print(f"Mejor Cromosoma: {mejor_cromosoma}\n")

        # 4. CREACIÓN DE LA NUEVA GENERACIÓN
        # Paso A: Elitismo - Preservar el 20% basado en FITNESS
        nueva_pob = obtener_elite_por_fitness(poblacion, fitness)
        
        # Paso B: Completar el 80% restante con Ruleta de 100 lugares
        while len(nueva_pob) < ag.POBLACION_TAM:
            # La ruleta usa el fitness para asignar los 100 casilleros
            p1 = opt_a.obtener_padre_ruleta(poblacion, fitness)
            p2 = opt_a.obtener_padre_ruleta(poblacion, fitness)
            
            # Cruce y Mutación manuales (desde motor_ag.py)
            h1, h2 = ag.cruce_un_punto(p1, p2)
            nueva_pob.append(ag.mutar_individuo(h1))
            
            if len(nueva_pob) < ag.POBLACION_TAM:
                nueva_pob.append(ag.mutar_individuo(h2))
        
        poblacion = nueva_pob

    # 5. Gráfico Final
    df = pd.DataFrame(historial)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Max_Obj'], label='Máximo F. Objetivo', color='blue', linewidth=2)
    plt.plot(df['Promedio_Obj'], label='Promedio F. Objetivo', color='green', linestyle='--')
    plt.plot(df['Desv_Fitness'], label='Desv. Est. Fitness', color='red')
    
    plt.title(f"Opción C: Elitismo (20% por Fitness) - {generaciones} Gen")
    plt.xlabel("Generación")
    plt.ylabel("Valores")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return df

if __name__ == "__main__":
    ejecutar_opcion_c(200)