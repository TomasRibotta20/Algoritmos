import os
import matplotlib.pyplot as plt

def graficar_recorrido(ciudades, recorrido, distancia_total, titulo, nombre_archivo):
    os.makedirs("mapas_resultados", exist_ok=True)

    lats = [ciudades[i]["lat"] for i in recorrido] + [ciudades[recorrido[0]]["lat"]]
    lons = [ciudades[i]["lon"] for i in recorrido] + [ciudades[recorrido[0]]["lon"]]

    plt.figure(figsize=(9, 12))
    plt.plot(lons, lats, "-o", color="#2c3e50", markerfacecolor="#e74c3c", markersize=6, linewidth=1.5)

    for indice in recorrido:
        ciudad = ciudades[indice]
        plt.annotate(ciudad["nombre"], (ciudad["lon"], ciudad["lat"]), fontsize=7, xytext=(3, 3), textcoords="offset points")

    plt.plot(lons[0], lats[0], marker="*", color="#f1c40f", markersize=18, markeredgecolor="black", zorder=5)

    plt.title(f"{titulo}\nDistancia total: {distancia_total:.2f} km")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"mapas_resultados/{nombre_archivo}")
    plt.close()
    print(f"-> Mapa guardado: mapas_resultados/{nombre_archivo}")

def graficar_evolucion_genetico(historial, nombre_archivo="genetico_evolucion.png"):
    os.makedirs("mapas_resultados", exist_ok=True)

    generaciones = [h["Gen"] for h in historial]
    mejores = [h["Mejor"] for h in historial]
    promedios = [h["Promedio"] for h in historial]
    peores = [h["Peor"] for h in historial]

    plt.figure(figsize=(10, 6))
    plt.plot(generaciones, mejores, label="Mejor distancia", color="#27ae60")
    plt.plot(generaciones, promedios, label="Distancia promedio", color="#2980b9")
    plt.plot(generaciones, peores, label="Peor distancia", color="#c0392b")
    plt.title("Evolución del Algoritmo Genético - Problema del Viajante")
    plt.xlabel("Generación")
    plt.ylabel("Distancia (km)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"mapas_resultados/{nombre_archivo}")
    plt.close()
    print(f"-> Gráfico guardado: mapas_resultados/{nombre_archivo}")
