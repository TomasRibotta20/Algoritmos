import motor_ag as ag
import random
import time
import sys

def obtener_padre_ruleta(poblacion, ruleta_vector):
    tiro = random.randint(0, 99)
    idx = ruleta_vector[tiro]
    return poblacion[idx], idx, tiro

def ejecutar_ruleta(generaciones, elitismo=False):
    generar_html = "--html" in sys.argv 
    
    inicio = time.time() # Inicia Cronómetro
    
    poblacion = ag.crear_poblacion()
    historial_stats = []
    historial_reporte = [] 
    
    mejor_global_val = float('-inf')
    mejor_global_crom = None
    gen_mejor_global = 0 

    for g in range(generaciones):
        objetivos = [ag.funcion_objetivo(ag.binario_a_decimal(ind)) for ind in poblacion]
        suma_obj = sum(objetivos)
        fitness = [o / suma_obj if suma_obj > 0 else 1/ag.POBLACION_TAM for o in objetivos]
        
        # Encontramos al mejor de esta generación en particular
        mejor_idx = objetivos.index(max(objetivos))
        mejor_crom = poblacion[mejor_idx]
        mejor_str = ''.join(str(b) for b in mejor_crom)
        mejor_decimal = ag.binario_a_decimal(mejor_crom)

        # Guardamos las estadísticas + info del cromosoma
        stats = {
            'Gen': g+1, 
            'Max': max(objetivos), 
            'Min': min(objetivos), 
            'Prom': suma_obj/ag.POBLACION_TAM, 
            'Desv_Fit': ag.calcular_desviacion_estandar(fitness),
            'Cromosoma_Max': mejor_str,
            'Decimal_Max': mejor_decimal
        }
        historial_stats.append(stats)
        
        if stats['Max'] > mejor_global_val:
            mejor_global_val = stats['Max']
            mejor_global_crom = mejor_crom[:]
            gen_mejor_global = g + 1

        casilleros = [max(1, int(f * 100)) if f > 0 else 0 for f in fitness]
        while sum(casilleros) != 100:
            idx = casilleros.index(max(casilleros))
            casilleros[idx] += 1 if sum(casilleros) < 100 else -1
            
        ruleta_vector = []
        for i, cant in enumerate(casilleros): ruleta_vector.extend([i] * cant)

        elite_guardada = ag.obtener_elite(poblacion, fitness) if elitismo else []
        
        if generar_html:
            gen_data = {
                'gen': g+1, 'poblacion': [ind[:] for ind in poblacion], 'objetivos': objetivos, 'fitness': fitness,
                'casilleros': casilleros, 'tiros': [], 'elite': elite_guardada, 'cruces': []
            }

        nueva_pob = []
        nueva_pob.extend(elite_guardada)

        while len(nueva_pob) < ag.POBLACION_TAM:
            p1, idx1, t1 = obtener_padre_ruleta(poblacion, ruleta_vector)
            p2, idx2, t2 = obtener_padre_ruleta(poblacion, ruleta_vector)
            
            h1, h2, punto = ag.cruce_un_punto(p1, p2)
            h1, m1 = ag.mutar_individuo(h1)
            h2, m2 = ag.mutar_individuo(h2)

            if generar_html:
                gen_data['tiros'].extend([t1, t2])
                gen_data['cruces'].append({
                    'p1': p1[:], 'idx1': idx1, 't1': t1, 'p2': p2[:], 'idx2': idx2, 't2': t2,
                    'punto': punto, 'h1': h1[:], 'm1': m1, 'h2': h2[:], 'm2': m2
                })

            nueva_pob.extend([h1, h2])
            
        poblacion = nueva_pob[:ag.POBLACION_TAM]
        
        if generar_html:
            historial_reporte.append(gen_data)

    tiempo_algoritmo = time.time() - inicio # Detiene Cronómetro

    # --- ZONA DE IMPRESIÓN Y EXPORTACIÓN ---
    mg_str = ''.join(str(b) for b in mejor_global_crom)
    mg_dec = ag.binario_a_decimal(mejor_global_crom)
    elitismo_estado = "Con Elitismo" if elitismo else "Sin Elitismo"
    
    print(f"\n[RULETA] {generaciones} Gen | {elitismo_estado}")
    print(f"Mejor global: {mejor_global_val:.6f} (Alcanzado en Gen {gen_mejor_global})")
    print(f"Cromosoma: {mg_str} (Decimal: {mg_dec}) | Tiempo: {tiempo_algoritmo:.4f} seg")
    
    ag.exportar_csv_generaciones(historial_stats, "Ruleta", generaciones, elitismo)
    ag.guardar_resumen_global("Ruleta", generaciones, elitismo, mejor_global_val, gen_mejor_global, tiempo_algoritmo)
    
    if generar_html:
        ag.generar_reporte_html(historial_reporte, "Ruleta", generaciones, elitismo)
    ag.graficar_y_guardar(historial_stats, "Ruleta", generaciones, elitismo, tiempo_algoritmo)

if __name__ == "__main__":
    ejecutar_ruleta(100)