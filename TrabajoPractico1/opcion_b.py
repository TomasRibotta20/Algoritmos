import motor_ag as ag
import random
import time

def seleccion_torneo(poblacion, fitness):
    k = max(2, int(ag.POBLACION_TAM * 0.4))
    def elegir_padre():
        indices = []
        while len(indices) < k:
            idx = random.randint(0, ag.POBLACION_TAM - 1)
            if idx not in indices: indices.append(idx)# Valida que no se repita el mismo individuo
        ganador = indices[0]
        for i in indices:
            if fitness[i] > fitness[ganador]: ganador = i
        return poblacion[ganador], ganador, indices
    return elegir_padre(), elegir_padre()

def ejecutar_torneo(generaciones, elitismo=False):
    inicio = time.time() # Inicia Cronometro
    poblacion = ag.crear_poblacion()
    historial_stats = []
    historial_reporte = []
    mejor_global_val = float('-inf')
    mejor_global_crom = None

    for g in range(generaciones):
        objetivos = [ag.funcion_objetivo(ag.binario_a_decimal(ind)) for ind in poblacion]
        suma_obj = sum(objetivos)
        fitness = [o / suma_obj if suma_obj > 0 else 1/ag.POBLACION_TAM for o in objetivos]
        
        # Estadísticas de Consola
        stats = {'Gen': g+1, 'Max': max(objetivos), 'Min': min(objetivos), 'Prom': suma_obj/ag.POBLACION_TAM, 'Desv_Fit': ag.calcular_desviacion_estandar(fitness)}
        historial_stats.append(stats)
        
        mejor_idx = objetivos.index(stats['Max'])
        mejor_crom = poblacion[mejor_idx]
        mejor_str = ''.join(str(b) for b in mejor_crom)
        mejor_decimal = ag.binario_a_decimal(mejor_crom)

        if stats['Max'] > mejor_global_val:
            mejor_global_val = stats['Max']
            mejor_global_crom = mejor_crom[:]

        # Print detallado en consola
        print(f"Gen {g+1:3} | MáxGen: {stats['Max']:.6f} | Min: {stats['Min']:.6f} | Prom: {stats['Prom']:.6f} | Desv Fit: {stats['Desv_Fit']:.6f} | MejorGen: {mejor_str} ({mejor_decimal})")

        elite_guardada = ag.obtener_elite(poblacion, fitness) if elitismo else []
        
        gen_data = {
            'gen': g+1, 'poblacion': [ind[:] for ind in poblacion], 'objetivos': objetivos, 'fitness': fitness,
            'elite': elite_guardada, 'cruces': []
        }

        nueva_pob = []
        nueva_pob.extend(elite_guardada)

        while len(nueva_pob) < ag.POBLACION_TAM:
            (p1, idx1, asp1), (p2, idx2, asp2) = seleccion_torneo(poblacion, fitness)
            
            h1, h2, punto = ag.cruce_un_punto(p1, p2)
            h1, m1 = ag.mutar_individuo(h1)
            h2, m2 = ag.mutar_individuo(h2)

            gen_data['cruces'].append({
                'p1': p1[:], 'idx1': idx1, 'asp1': asp1, 'p2': p2[:], 'idx2': idx2, 'asp2': asp2,
                'punto': punto, 'h1': h1[:], 'm1': m1, 'h2': h2[:], 'm2': m2
            })

            nueva_pob.extend([h1, h2])
            
        poblacion = nueva_pob[:ag.POBLACION_TAM]
        historial_reporte.append(gen_data)

    tiempo_algoritmo = time.time() - inicio # Detiene Cronometro

    # Cierre de Consola
    print("\nMejor global:")
    mg_str = ''.join(str(b) for b in mejor_global_crom)
    mg_dec = ag.binario_a_decimal(mejor_global_crom)
    print(f"Valor objetivo: {mejor_global_val:.6f} | Cromosoma: {mg_str} (Valor Decimal:{mg_dec})")
    elitismo_estado = "Con Elitismo" if elitismo else "Sin Elitismo"
    print(f"Tiempo de compilacion Torneo {generaciones} Generaciones {elitismo_estado}: {tiempo_algoritmo:.4f} seg")
    
    # Renderizado y Guardado Visual
    ag.generar_reporte_html(historial_reporte, "Torneo", generaciones, elitismo)
    ag.graficar_y_guardar(historial_stats, "Torneo", generaciones, elitismo, tiempo_algoritmo)

if __name__ == "__main__":
    ejecutar_torneo(200)