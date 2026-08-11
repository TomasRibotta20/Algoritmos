import time
import csv

# ============================================================
# EJERCICIO 1: BÚSQUEDA EXHAUSTIVA (10 objetos, volumen)
# ============================================================

def busqueda_exhaustiva(volumenes, valores, capacidad_max):
    n = len(volumenes)
    total_subconjuntos = 2 ** n

    # Estructura donde se guardan TODOS los subconjuntos generados
    todos_los_subconjuntos = []

    for numero in range(total_subconjuntos):
        objetos_incluidos = []
        volumen_total = 0
        valor_total = 0

        for i in range(n):
            bit = (numero >> i) & 1
            if bit == 1:
                objetos_incluidos.append(i)
                volumen_total += volumenes[i]
                valor_total += valores[i]

        todos_los_subconjuntos.append({
            "objetos": objetos_incluidos,
            "volumen": volumen_total,
            "valor": valor_total,
        })

    # Ahora que estan TODOS los subconjuntos generados y evaluados,
    # se pasa a una segunda estructura solo el mejor subconjunto valido.
    mejor_subconjunto = None
    for subconjunto in todos_los_subconjuntos:
        if subconjunto["volumen"] <= capacidad_max:
            if mejor_subconjunto is None or subconjunto["valor"] > mejor_subconjunto["valor"]:
                mejor_subconjunto = subconjunto

    return mejor_subconjunto, todos_los_subconjuntos


# ============================================================
# EJERCICIO 2: ALGORITMO GREEDY (10 objetos, volumen)
# ============================================================

def algoritmo_greedy(volumenes, valores, capacidad_max):
    n = len(volumenes)

    # Se calcula el ratio $/cm3 de cada objeto
    objetos = []
    for i in range(n):
        ratio = valores[i] / volumenes[i]
        objetos.append({"indice": i, "volumen": volumenes[i], "valor": valores[i], "ratio": ratio})

    objetos.sort(key=lambda obj: obj["ratio"], reverse=True)

    volumen_acumulado = 0
    valor_acumulado = 0
    seleccionados = []

    for obj in objetos:
        if volumen_acumulado + obj["volumen"] <= capacidad_max:
            seleccionados.append(obj["indice"])
            volumen_acumulado += obj["volumen"]
            valor_acumulado += obj["valor"]
        # si no entra, se descarta y se sigue probando con el siguiente

    resultado = {
        "objetos": seleccionados,
        "volumen": volumen_acumulado,
        "valor": valor_acumulado,
    }

    return resultado, objetos  # objetos ya trae el ratio calculado y ordenado


# ============================================================
# FUNCIONES AUXILIARES DE IMPRESION
# ============================================================

def mostrar_subconjunto(nombre, subconjunto, offset_indices=1):
    objetos_mostrados = [i + offset_indices for i in subconjunto["objetos"]]
    print(f"{nombre}:")
    print(f"  Objetos incluidos : {objetos_mostrados}")
    print(f"  Volumen total     : {subconjunto['volumen']}")
    print(f"  Valor total       : {subconjunto['valor']}")


# ============================================================
# FUNCIONES AUXILIARES DE EXPORTACION A CSV
# ============================================================

def guardar_csv(nombre_archivo, encabezados, filas):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        escritor.writerows(filas)
    print(f"  -> Guardado: {nombre_archivo}")


def exportar_subconjuntos_csv(nombre_archivo, todos_los_subconjuntos, capacidad_max, mejor_subconjunto, offset_indices=1):
    encabezados = ["subconjunto_binario", "objetos", "volumen_total", "valor_total", "valido", "es_optimo"]
    filas = []
    n = len(bin(len(todos_los_subconjuntos) - 1)) - 2  # cantidad de bits necesarios
    for indice, subconjunto in enumerate(todos_los_subconjuntos):
        objetos_mostrados = [i + offset_indices for i in subconjunto["objetos"]]
        texto_objetos = ", ".join(str(o) for o in objetos_mostrados) if objetos_mostrados else "Ninguno"
        binario = format(indice, f"0{n}b")
        valido = subconjunto["volumen"] <= capacidad_max
        es_optimo = subconjunto is mejor_subconjunto
        filas.append([binario, texto_objetos, subconjunto["volumen"], subconjunto["valor"], valido, es_optimo])
    guardar_csv(nombre_archivo, encabezados, filas)


def exportar_orden_greedy_csv(nombre_archivo, objetos_ordenados, seleccionados, offset_indices=1):
    encabezados = ["orden", "objeto", "volumen", "valor", "ratio", "seleccionado"]
    filas = []
    seleccionados_set = set(seleccionados)
    for posicion, obj in enumerate(objetos_ordenados, start=1):
        filas.append([
            posicion,
            obj["indice"] + offset_indices,
            obj["volumen"],
            obj["valor"],
            round(obj["ratio"], 4),
            obj["indice"] in seleccionados_set,
        ])
    guardar_csv(nombre_archivo, encabezados, filas)


def exportar_comparacion_csv(nombre_archivo, filas_comparacion):
    encabezados = ["ejercicio", "metodo", "objetos", "capacidad_usada", "valor_total", "tiempo_segundos", "alcanzo_optimo"]
    guardar_csv(nombre_archivo, encabezados, filas_comparacion)


# ============================================================
# EJERCICIOS 1 y 2: 10 OBJETOS, RESTRICCION DE VOLUMEN
# ============================================================

def ejercicios_1_y_2(filas_comparacion):
    print("=" * 60)
    print("EJERCICIOS 1 y 2 - 10 objetos - Capacidad 4200 cm3")
    print("=" * 60)

    # Objeto 1..10 -> indices 0..9
    volumenes = [150, 325, 600, 805, 430, 1200, 770, 60, 930, 353]
    valores =   [20,  40,  50,  36,  25,  64,   54,  18, 46,  28]
    capacidad_max = 4200

    # --- Busqueda exhaustiva ---
    inicio = time.perf_counter()
    mejor_exhaustivo, todos = busqueda_exhaustiva(volumenes, valores, capacidad_max)
    fin = time.perf_counter()
    tiempo_exhaustivo = fin - inicio

    print(f"\nCantidad de subconjuntos evaluados: {len(todos)} (2^10)")
    mostrar_subconjunto("\nMejor solucion - Busqueda Exhaustiva", mejor_exhaustivo)
    print(f"  Tiempo de ejecucion: {tiempo_exhaustivo:.6f} segundos")

    # --- Algoritmo Greedy ---
    inicio = time.perf_counter()
    resultado_greedy, objetos_ordenados = algoritmo_greedy(volumenes, valores, capacidad_max)
    fin = time.perf_counter()
    tiempo_greedy = fin - inicio

    print("\nOrden de objetos segun ratio valor/volumen (mayor a menor):")
    for obj in objetos_ordenados:
        print(f"  Objeto {obj['indice']+1}: volumen={obj['volumen']}, "
              f"valor={obj['valor']}, ratio={obj['ratio']:.4f}")

    mostrar_subconjunto("\nSolucion - Algoritmo Greedy", resultado_greedy)
    print(f"  Tiempo de ejecucion: {tiempo_greedy:.6f} segundos")

    # --- Comparacion ---
    print("\n--- Comparacion Ejercicios 1 y 2 ---")
    print(f"Valor optimo (exhaustivo) : {mejor_exhaustivo['valor']}")
    print(f"Valor obtenido (greedy)   : {resultado_greedy['valor']}")
    alcanzo_optimo = resultado_greedy["valor"] == mejor_exhaustivo["valor"]
    if alcanzo_optimo:
        print("-> El greedy SI alcanzo el valor optimo en este caso.")
    else:
        diferencia = mejor_exhaustivo["valor"] - resultado_greedy["valor"]
        print(f"-> El greedy NO alcanzo el optimo. Diferencia: {diferencia}")
    print(f"Tiempo exhaustivo: {tiempo_exhaustivo:.6f} s vs. Tiempo greedy: {tiempo_greedy:.6f} s")

    # --- Exportacion a CSV ---
    print("\nExportando resultados a CSV...")
    exportar_subconjuntos_csv("ejercicio1_subconjuntos.csv", todos, capacidad_max, mejor_exhaustivo)
    exportar_orden_greedy_csv("ejercicio2_orden_greedy.csv", objetos_ordenados, resultado_greedy["objetos"])

    filas_comparacion.append([
        "1 y 2", "Busqueda Exhaustiva",
        ", ".join(str(i + 1) for i in mejor_exhaustivo["objetos"]),
        mejor_exhaustivo["volumen"], mejor_exhaustivo["valor"], round(tiempo_exhaustivo, 8), True,
    ])
    filas_comparacion.append([
        "1 y 2", "Greedy",
        ", ".join(str(i + 1) for i in resultado_greedy["objetos"]),
        resultado_greedy["volumen"], resultado_greedy["valor"], round(tiempo_greedy, 8), alcanzo_optimo,
    ])


# ============================================================
# EJERCICIO 3: 3 ELEMENTOS, RESTRICCION DE PESO
# ============================================================

def ejercicio_3(filas_comparacion):
    print("\n" + "=" * 60)
    print("EJERCICIO 3 - 3 elementos - Capacidad 3000 grs")
    print("=" * 60)

    # Elemento 1..3 -> indices 0..2
    pesos = [1800, 600, 1200]
    valores = [72, 36, 60]
    capacidad_max = 3000

    # --- Busqueda exhaustiva ---
    inicio = time.perf_counter()
    mejor_exhaustivo, todos = busqueda_exhaustiva(pesos, valores, capacidad_max)
    fin = time.perf_counter()
    tiempo_exhaustivo = fin - inicio

    print(f"\nCantidad de subconjuntos evaluados: {len(todos)} (2^3)")
    for subconjunto in todos:
        objetos_mostrados = [i + 1 for i in subconjunto["objetos"]]
        texto_objetos = str(objetos_mostrados) if objetos_mostrados else "Ninguno"
        valido = "valido" if subconjunto["volumen"] <= capacidad_max else "excede capacidad"
        print(f"  {texto_objetos:<12} "
              f"peso={subconjunto['volumen']:<6} valor={subconjunto['valor']:<5} ({valido})")

    mostrar_subconjunto("\nMejor solucion - Busqueda Exhaustiva", mejor_exhaustivo)
    print(f"  Tiempo de ejecucion: {tiempo_exhaustivo:.8f} segundos")

    # --- Algoritmo Greedy ---
    inicio = time.perf_counter()
    resultado_greedy, objetos_ordenados = algoritmo_greedy(pesos, valores, capacidad_max)
    fin = time.perf_counter()
    tiempo_greedy = fin - inicio

    print("\nOrden de elementos segun ratio valor/peso (mayor a menor):")
    for obj in objetos_ordenados:
        print(f"  Elemento {obj['indice']+1}: peso={obj['volumen']}, "
              f"valor={obj['valor']}, ratio={obj['ratio']:.4f}")

    mostrar_subconjunto("\nSolucion - Algoritmo Greedy", resultado_greedy)
    print(f"  Tiempo de ejecucion: {tiempo_greedy:.8f} segundos")

    # --- Comparacion ---
    print("\n--- Comparacion Ejercicio 3 ---")
    print(f"Valor optimo (exhaustivo) : {mejor_exhaustivo['valor']}")
    print(f"Valor obtenido (greedy)   : {resultado_greedy['valor']}")
    alcanzo_optimo = resultado_greedy["valor"] == mejor_exhaustivo["valor"]
    if alcanzo_optimo:
        print("-> El greedy SI alcanzo el valor optimo en este caso.")
    else:
        diferencia = mejor_exhaustivo["valor"] - resultado_greedy["valor"]
        print(f"-> El greedy NO alcanzo el optimo. Diferencia: {diferencia}")
        print("   Esto pasa porque el greedy elige por ratio valor/peso paso a paso")
        print("   y ese criterio local no siempre lleva a la mejor combinacion global.")

    # --- Exportacion a CSV ---
    print("\nExportando resultados a CSV...")
    exportar_subconjuntos_csv("ejercicio3_subconjuntos.csv", todos, capacidad_max, mejor_exhaustivo)
    exportar_orden_greedy_csv("ejercicio3_orden_greedy.csv", objetos_ordenados, resultado_greedy["objetos"])

    filas_comparacion.append([
        "3", "Busqueda Exhaustiva",
        ", ".join(str(i + 1) for i in mejor_exhaustivo["objetos"]),
        mejor_exhaustivo["volumen"], mejor_exhaustivo["valor"], round(tiempo_exhaustivo, 8), True,
    ])
    filas_comparacion.append([
        "3", "Greedy",
        ", ".join(str(i + 1) for i in resultado_greedy["objetos"]),
        resultado_greedy["volumen"], resultado_greedy["valor"], round(tiempo_greedy, 8), alcanzo_optimo,
    ])


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    filas_comparacion = []

    ejercicios_1_y_2(filas_comparacion)
    ejercicio_3(filas_comparacion)

    print("\n" + "=" * 60)
    print("Exportando tabla comparativa general...")
    exportar_comparacion_csv("comparacion_general.csv", filas_comparacion)
    print("=" * 60)