# Informe del Trabajo Práctico N°3: El Problema del Viajante (TSP)

## Ejercicio 1 – Método Exhaustivo (Justificación Teórica)
El Problema del Viajante de Comercio (TSP) busca encontrar la ruta más corta que visite todas las ciudades exactamente una vez y regrese al origen. Para un conjunto de N ciudades, la cantidad de rutas posibles (permutaciones circulares sin considerar la dirección de recorrido) está dada por la fórmula:

$$ \frac{(N - 1)!}{2} $$

Para este problema contamos con **N = 23** capitales provinciales. Aplicando la fórmula:
$$ \frac{(23 - 1)!}{2} = \frac{22!}{2} \approx 5.62 \times 10^{20} \text{ rutas posibles.} $$

Si asumiéramos que una computadora estándar de alta capacidad es capaz de evaluar 1.000.000.000 ($10^9$) rutas por segundo, el tiempo que le tomaría evaluar todas las combinaciones sería:
$$ \frac{5.62 \times 10^{20}}{10^9} = 5.62 \times 10^{11} \text{ segundos.} $$

Esto equivale a aproximadamente **1.78 × 10⁴ años** (¡más de 17.000 años!).

**Conclusión:** Resolver el TSP para 23 ciudades mediante un método de búsqueda exhaustiva (fuerza bruta) resulta inviable computacionalmente en un tiempo razonable. Es por ello que en la práctica se debe recurrir a algoritmos de aproximación, heurísticas (como el vecino más cercano) o metaheurísticas (como los algoritmos genéticos).

---

## Resultados Obtenidos y Comparación

### Heurística del Vecino Más Cercano
Se evaluó el método partiendo desde cada una de las 23 capitales, buscando de forma voraz la ciudad no visitada más cercana, para luego determinar el mejor punto de partida global:
- **Mejor recorrido (Partiendo desde Neuquén):** 10.364,00 km
- **Ruta:** Neuquén -> Santa Rosa -> San Luis -> Mendoza -> San Juan -> La Rioja -> S.F.V. de Catamarca -> Sgo. del Estero -> S.M. de Tucumán -> Salta -> S.S. de Jujuy -> Resistencia -> Corrientes -> Formosa -> Posadas -> Paraná -> Santa Fe -> Córdoba -> La Plata -> Viedma -> Rawson -> Río Gallegos -> Ushuaia -> Neuquén

### Algoritmo Genético
Se realizaron 10 ejecuciones independientes utilizando una población de $N = 50$ individuos, iterando durante $M = 200$ generaciones (ciclos). Se utilizó Crossover Cíclico (CX) con una tasa de cruza del 80% y mutación por intercambio (swap) con una tasa del 10%:
- **Mejor resultado en 10 ejecuciones:** 11.323,00 km
- **Promedio de los resultados:** 12.536,10 km
- **Peor resultado:** 13.603,00 km

### Comparación
En los experimentos realizados, la heurística del Vecino Más Cercano demostró ser mejor y más eficiente que el Algoritmo Genético propuesto en la consigna. La heurística logró una distancia mínima de **10.364,00 km**, siendo superior por un **8,5% (~959 km)** respecto al mejor resultado obtenido por el algoritmo genético (11.323,00 km).
Cabe destacar que el AG estuvo limitado a solo 50 individuos y 200 ciclos. Dado el inmenso espacio de búsqueda ($5.6 \times 10^{20}$), la convergencia hacia un óptimo requiere un esfuerzo computacional (y de parámetros) mucho mayor que el que plantea la configuración solicitada, mientras que el Vecino Más Cercano obtiene un camino "suficientemente bueno" en cuestión de milisegundos.

---

## Aportes Prácticos del TSP

El Problema del Viajante (TSP) es uno de los problemas NP-hard más estudiados en la ciencia de la computación, no solo por su complejidad matemática, sino porque modela de manera excelente innumerables problemas del mundo real. A continuación, se explican algunas de sus aplicaciones más importantes en la actualidad:

1. **Logística y Distribución de Última Milla:**
   Empresas de comercio electrónico, servicios de paquetería (como Amazon, Mercado Libre, FedEx o UPS) y servicios postales emplean algoritmos basados en variaciones del TSP. Cada repartidor debe entregar múltiples paquetes en distintas ubicaciones dentro de una ciudad y regresar al centro de distribución o almacén. Calcular el recorrido que minimice la distancia y el tiempo de viaje reduce drásticamente el consumo de combustible, los costos de operación y las emisiones de carbono, a la vez que maximiza la cantidad de entregas diarias.

2. **Fabricación de Circuitos Impresos (PCB) y Microchips:**
   En la industria electrónica, la fabricación de placas madre (motherboards) o microchips requiere perforar orificios o soldar pequeños componentes en cientos o miles de ubicaciones precisas a lo largo de la placa. El cabezal láser, taladro robótico o brazo soldador debe visitar cada uno de estos puntos de la forma más eficiente posible. Modelar el recorrido del brazo robótico como un Problema del Viajante minimiza la distancia total que el cabezal se mueve "en el aire", lo cual reduce los tiempos muertos de producción y acelera enormemente la fabricación a gran escala.

3. **Planificación de Rutas para Drones y Vehículos Autónomos:**
   En áreas como la agricultura de precisión (donde drones recorren campos para esparcir fertilizantes o monitorear cultivos) o en tareas de inspección de infraestructuras (como revisar torres eléctricas, oleoductos o realizar cartografía), los vehículos autónomos deben recorrer múltiples puntos de interés predefinidos. Debido a que las baterías limitan severamente el tiempo de vuelo de los drones, optimizar la ruta para que sea la más corta posible garantiza que el equipo pueda cumplir toda su misión de inspección y retornar seguro a la estación base antes de quedarse sin energía.
