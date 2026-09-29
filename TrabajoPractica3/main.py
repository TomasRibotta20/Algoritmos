import time
import csv
import os

from ciudades import CIUDADES
from distancias import construir_matriz_distancias
import exhaustivo
import heuristica
import genetico
import visualizacion

def mostrar_recorrido(recorrido, distancia):
    nombres = [CIUDADES[i]["nombre"] for i in recorrido]
    print(" -> ".join(nombres) + f" -> {nombres[0]}")
    print(f"Distancia total: {distancia:.2f} km")

def seleccionar_ciudad_inicio():
    print("\nCapitales disponibles:")
    for i, ciudad in enumerate(CIUDADES):
        print(f"  {i + 1}. {ciudad['nombre']} ({ciudad['provincia']})")
    while True:
        entrada = input("\nIngrese el número de la capital de partida: ")
        if entrada.isdigit() and 1 <= int(entrada) <= len(CIUDADES):
            return int(entrada) - 1
        print("Opción inválida, intente nuevamente.")

def opcion_1_exhaustivo():
    print("\n=== EJERCICIO 1: MÉTODO EXHAUSTIVO ===")
    exhaustivo.justificacion_teorica(len(CIUDADES))

    print("\nDemostración del método sobre un subconjunto reducido de 8 capitales:")
    matriz = construir_matriz_distancias(CIUDADES)
    inicio_tiempo = time.time()
    recorrido, distancia = exhaustivo.demo_reducida(matriz, cantidad=8)
    tiempo = time.time() - inicio_tiempo
    mostrar_recorrido(recorrido, distancia)
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

def opcion_2a_heuristica_manual(matriz):
    print("\n=== EJERCICIO 2.a: HEURÍSTICA - CIUDAD A ELECCIÓN ===")
    ciudad_inicio = seleccionar_ciudad_inicio()
    inicio_tiempo = time.time()
    recorrido = heuristica.vecino_mas_cercano(ciudad_inicio, matriz, len(CIUDADES))
    distancia = heuristica.longitud_recorrido(recorrido, matriz)
    tiempo = time.time() - inicio_tiempo

    print(f"\nCiudad de partida: {CIUDADES[ciudad_inicio]['nombre']}")
    mostrar_recorrido(recorrido, distancia)
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")

    visualizacion.graficar_recorrido(
        CIUDADES, recorrido, distancia,
        f"Recorrido Heurístico - Partida: {CIUDADES[ciudad_inicio]['nombre']}",
        f"heuristica_{CIUDADES[ciudad_inicio]['nombre'].replace(' ', '_')}.png",
    )
    return recorrido, distancia

def opcion_2b_heuristica_optima(matriz):
    print("\n=== EJERCICIO 2.b: HEURÍSTICA - MEJOR PUNTO DE PARTIDA ===")
    inicio_tiempo = time.time()
    mejor_inicio, mejor_recorrido, mejor_distancia, resultados = heuristica.mejor_recorrido_todas_las_capitales(matriz, len(CIUDADES))
    tiempo = time.time() - inicio_tiempo

    print("\nResultados por ciudad de partida:")
    for inicio, recorrido, distancia in resultados:
        print(f"  {CIUDADES[inicio]['nombre']:<40} {distancia:.2f} km")

    print(f"\nMejor ciudad de partida: {CIUDADES[mejor_inicio]['nombre']}")
    mostrar_recorrido(mejor_recorrido, mejor_distancia)
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

    visualizacion.graficar_recorrido(
        CIUDADES, mejor_recorrido, mejor_distancia,
        f"Mejor Recorrido Heurístico - Partida: {CIUDADES[mejor_inicio]['nombre']}",
        "heuristica_mejor_global.png",
    )

    guardar_csv_heuristica(resultados)
    return mejor_recorrido, mejor_distancia

def opcion_2c_genetico(matriz):
    print("\n=== EJERCICIO 2.c: ALGORITMO GENÉTICO ===")
    inicio_tiempo = time.time()
    mejor_recorrido, mejor_distancia, historial = genetico.ejecutar_algoritmo_genetico(matriz, len(CIUDADES))
    tiempo = time.time() - inicio_tiempo

    mostrar_recorrido(mejor_recorrido, mejor_distancia)
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")

    visualizacion.graficar_recorrido(
        CIUDADES, mejor_recorrido, mejor_distancia,
        "Mejor Recorrido - Algoritmo Genético",
        "genetico_mejor_recorrido.png",
    )
    visualizacion.graficar_evolucion_genetico(historial)
    guardar_csv_genetico(historial)
    return mejor_recorrido, mejor_distancia

def guardar_csv_heuristica(resultados):
    os.makedirs("csv_resultados", exist_ok=True)
    with open("csv_resultados/heuristica_todas_las_capitales.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["ciudad_partida", "distancia_km"])
        for inicio, recorrido, distancia in resultados:
            escritor.writerow([CIUDADES[inicio]["nombre"], round(distancia, 2)])
    print("-> CSV guardado: csv_resultados/heuristica_todas_las_capitales.csv")

def guardar_csv_genetico(historial):
    os.makedirs("csv_resultados", exist_ok=True)
    with open("csv_resultados/genetico_evolucion.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["generacion", "mejor_km", "promedio_km", "peor_km"])
        for fila in historial:
            escritor.writerow([fila["Gen"], round(fila["Mejor"], 2), round(fila["Promedio"], 2), round(fila["Peor"], 2)])
    print("-> CSV guardado: csv_resultados/genetico_evolucion.csv")

def guardar_csv_comparacion(distancia_heuristica, distancia_genetico):
    os.makedirs("csv_resultados", exist_ok=True)
    diferencia = distancia_heuristica - distancia_genetico
    porcentaje = (diferencia / distancia_heuristica) * 100 if distancia_heuristica > 0 else 0

    with open("csv_resultados/comparacion_final.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["metodo", "distancia_km"])
        escritor.writerow(["Heurística (vecino más cercano)", round(distancia_heuristica, 2)])
        escritor.writerow(["Algoritmo Genético", round(distancia_genetico, 2)])
    print("-> CSV guardado: csv_resultados/comparacion_final.csv")

    if diferencia > 0:
        print(f"\nEl AG mejoró a la heurística por {diferencia:.2f} km ({porcentaje:.2f}%).")
    else:
        print(f"\nLa heurística obtuvo un resultado {abs(diferencia):.2f} km mejor que el AG en esta corrida.")

def mostrar_menu():
    matriz = construir_matriz_distancias(CIUDADES)
    distancia_heuristica_global = None
    distancia_genetico_global = None

    while True:
        print("\n" + "=" * 60)
        print("TP - PROBLEMA DEL VIAJANTE - CAPITALES DE ARGENTINA")
        print("=" * 60)
        print("1. Ejercicio 1 - Método Exhaustivo (justificación teórica + demo)")
        print("2. Ejercicio 2.a - Heurística desde una capital a elección")
        print("3. Ejercicio 2.b - Heurística probando todas las capitales de partida")
        print("4. Ejercicio 2.c - Algoritmo Genético")
        print("5. Comparar Heurística vs Algoritmo Genético")
        print("0. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            opcion_1_exhaustivo()
        elif opcion == "2":
            opcion_2a_heuristica_manual(matriz)
        elif opcion == "3":
            _, distancia_heuristica_global = opcion_2b_heuristica_optima(matriz)
        elif opcion == "4":
            _, distancia_genetico_global = opcion_2c_genetico(matriz)
        elif opcion == "5":
            if distancia_heuristica_global is None:
                print("\nPrimero debe ejecutar la opción 3 (Heurística - todas las capitales).")
                continue
            if distancia_genetico_global is None:
                print("\nPrimero debe ejecutar la opción 4 (Algoritmo Genético).")
                continue
            guardar_csv_comparacion(distancia_heuristica_global, distancia_genetico_global)
        elif opcion == "0":
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción inválida.")

if __name__ == "__main__":
    mostrar_menu()
