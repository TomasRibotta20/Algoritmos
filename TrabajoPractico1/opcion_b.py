import motor_ag as ag
import random
import time

def seleccion_torneo(poblacion, fitness):
    k = max(2, int(ag.POBLACION_TAM * 0.4))
    def elegir_padre():
        indices = []
        while len(indices) < k:
            idx = random.randint(0, ag.POBLACION_TAM - 1)
            if idx not in indices: indices.append(idx)# Validamos que el mismo individuo no participe más de una vez en el torneo
        
        ganador = indices[0]
        for i in indices:
            if fitness[i] > fitness[ganador]: ganador = i
        return poblacion[ganador]
    return elegir_padre(), elegir_padre()

def ejecutar_torneo(generaciones, elitismo=False):
    inicio = time.time()
    poblacion = ag.crear_poblacion()
    historial = []
    mejor_global_val = float('-inf')
    mejor_global_crom = None

    for g in range(generaciones):
        objetivos = [ag.funcion_objetivo(ag.binario_a_decimal(ind)) for ind in poblacion]
        suma_obj = sum(objetivos)
        fitness = [o / suma_obj if suma_obj > 0 else 1/ag.POBLACION_TAM for o in objetivos]
        
        stats = {'Gen': g+1, 'Max': max(objetivos), 'Min': min(objetivos), 
                 'Prom': suma_obj/ag.POBLACION_TAM, 'Desv_Fit': ag.calcular_desviacion_estandar(fitness)}
        historial.append(stats)
        
        # Mejor cromosoma de la generación (como ceros y unos) y su valor decimal
        mejor_idx = objetivos.index(stats['Max'])
        mejor_crom = poblacion[mejor_idx]
        mejor_str = ''.join(str(b) for b in mejor_crom)
        mejor_decimal = ag.binario_a_decimal(mejor_crom)

        # Actualizar mejor global
        if stats['Max'] > mejor_global_val:
            mejor_global_val = stats['Max']
            mejor_global_crom = mejor_crom[:]

        print(f"Gen {g+1:3} | MáxGen: {stats['Max']:.6f} | Min: {stats['Min']:.6f} | Prom: {stats['Prom']:.6f} | Desv Fit: {stats['Desv_Fit']:.6f} | MejorGen: {mejor_str} ({mejor_decimal})")

        nueva_pob = ag.obtener_elite(poblacion, fitness) if elitismo else []
        while len(nueva_pob) < ag.POBLACION_TAM:
            p1, p2 = seleccion_torneo(poblacion, fitness)
            h1, h2 = ag.cruce_un_punto(p1, p2)
            nueva_pob.extend([ag.mutar_individuo(h1), ag.mutar_individuo(h2)])
        poblacion = nueva_pob[:ag.POBLACION_TAM]


    if mejor_global_crom is not None:
        print("\nMejor global:")
        mg_str = ''.join(str(b) for b in mejor_global_crom)
        mg_dec = ag.binario_a_decimal(mejor_global_crom)
        print(f"Valor objetivo: {mejor_global_val:.6f} | Cromosoma: {mg_str} (Valor Decimal:{mg_dec})")
    tiempo = time.time() - inicio
    elitismo_estado = "Con Elitismo" if elitismo else "Sin Elitismo"
    print(f"Tiempo de compilacion Torneo {generaciones} Generaciones {elitismo_estado}: {tiempo:.4f} seg") 
    ag.graficar_y_guardar(historial, "Torneo", generaciones, elitismo)

if __name__ == "__main__":
    ejecutar_torneo(100)