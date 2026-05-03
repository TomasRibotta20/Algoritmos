import motor_ag as ag
import random
import time

def obtener_padre_ruleta(poblacion, fitness):
    ruleta_vector = []
    casilleros = [max(1, int(f * 100)) if f > 0 else 0 for f in fitness]#Otorga casilleros segun el fitness, validando que tengan al menos 1 cada individuo
    
    while sum(casilleros) != 100:
        idx = casilleros.index(max(casilleros))
        casilleros[idx] += 1 if sum(casilleros) < 100 else -1
            
    for i, cant in enumerate(casilleros):
        ruleta_vector.extend([i] * cant)

    return poblacion[ruleta_vector[random.randint(0, 99)]] #Retornamos el individuo seleccionado al azar segun la ruleta creada

def ejecutar_ruleta(generaciones, elitismo=False):
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
        
        # Mejor cromosoma de la generación (ceros y unos) y su valor decimal
        mejor_idx = objetivos.index(stats['Max'])
        mejor_crom = poblacion[mejor_idx]
        mejor_str = ''.join(str(b) for b in mejor_crom)
        mejor_decimal = ag.binario_a_decimal(mejor_crom)

        # Actualizar mejor global si corresponde
        if stats['Max'] > mejor_global_val:
            mejor_global_val = stats['Max']
            mejor_global_crom = mejor_crom[:]

        print(f"Gen {g:3} | MáxGen: {stats['Max']:.6f} | Min: {stats['Min']:.6f} | Prom: {stats['Prom']:.6f} | Desv Fit: {stats['Desv_Fit']:.6f} | MejorGen: {mejor_str} ({mejor_decimal})")

        nueva_pob = ag.obtener_elite(poblacion, fitness) if elitismo else []
        while len(nueva_pob) < ag.POBLACION_TAM:
            p1, p2 = obtener_padre_ruleta(poblacion, fitness), obtener_padre_ruleta(poblacion, fitness)
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
    print(f"Tiempo de compilacion Ruleta {generaciones} Generaciones {elitismo_estado}: {tiempo:.4f} seg")    
    ag.graficar_y_guardar(historial, "Ruleta", generaciones, elitismo, tiempo)

if __name__ == "__main__":
    ejecutar_ruleta(100)