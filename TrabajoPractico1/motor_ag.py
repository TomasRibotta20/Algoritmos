import random
import matplotlib.pyplot as plt
import pandas as pd
import os

CANT_GENES = 30
POBLACION_TAM = 10
COEF = 2**30 - 1
PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05

def funcion_objetivo(valor_decimal):
    return (valor_decimal / COEF) ** 2

def binario_a_decimal(cromosoma):
    decimal = 0
    for i in range(len(cromosoma)):
        bit = cromosoma[i]
        potencia = (len(cromosoma) - 1) - i
        if bit == 1:
            decimal += 2 ** potencia
    return decimal

def calcular_desviacion_estandar(valores):
    n = len(valores)
    if n == 0: return 0
    promedio = sum(valores) / n
    suma_cuadrados = sum((x - promedio) ** 2 for x in valores)
    return (suma_cuadrados / n) ** 0.5

def cruce_un_punto(p1, p2):
    if random.random() < PROB_CROSSOVER:
        punto = random.randint(1, CANT_GENES - 1)
        return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:], punto
    return p1[:], p2[:], None

def mutar_individuo(cromosoma):
    if random.random() < PROB_MUTACION:
        pos = random.randint(0, CANT_GENES - 1)
        cromosoma[pos] = 1 - cromosoma[pos]
        return cromosoma, pos
    return cromosoma, None

def crear_poblacion():
    return [[random.randint(0, 1) for _ in range(CANT_GENES)] for _ in range(POBLACION_TAM)]

def obtener_elite(poblacion, fitness):
    cantidad = max(2, int(POBLACION_TAM * 0.2))
    combinado = sorted(zip(poblacion, fitness), key=lambda x: x[1], reverse=True)
    return [c[0][:] for c in combinado[:cantidad]]

def graficar_y_guardar(historial, metodo, generaciones, elitismo, tiempo):
    df = pd.DataFrame(historial)
    os.makedirs("graficos_resultados", exist_ok=True)
    
    plt.figure(figsize=(10, 7))
    plt.plot(df['Max'], label="Máximo Obj")
    plt.plot(df['Min'], label="Mínimo Obj")
    plt.plot(df['Prom'], label="Promedio Obj")
    plt.plot(df['Desv_Fit'], label="Desv. Est. Fitness", color='red')
    
    estado_elitismo = "Si" if elitismo else "No"
    params = f"Población: {POBLACION_TAM} | Pc: {PROB_CROSSOVER} | Pm: {PROB_MUTACION}"
    plt.title(f"Método: {metodo} | Gen: {generaciones} | Elitismo: {estado_elitismo} | Tiempo: {tiempo:.4f} seg\n{params}")
    plt.xlabel("Generación"); plt.ylabel("Valor")
    plt.legend(); plt.grid(True)
    
    nombre_arch = f"{metodo}_{generaciones}gen_elitismo_{estado_elitismo}.png"
    plt.savefig(f"graficos_resultados/{nombre_arch}")
    plt.close()

# =====================================================================
# BLOQUE DE CONSTRUCCIÓN VISUAL 
# =====================================================================

def _html_cromosoma(cromosoma, punto_corte=None, pos_mutacion=None):
    html = "<div class='cromosoma'>"
    for i, bit in enumerate(cromosoma):
        clases = "bit"
        if punto_corte is not None and i == punto_corte: clases += " corte"
        if pos_mutacion is not None and i == pos_mutacion: clases += " mutado"
        html += f"<div class='{clases}'>{bit}</div>"
    html += "</div>"
    return html

def _html_barra_ruleta(casilleros, tiros):
    html = "<div style='position: relative; margin-top: 30px; margin-bottom: 20px;'>"
    for i, tiro in enumerate(tiros):
        html += f"<div class='tiro-label' style='left: {tiro}%;'>T{i+1}</div>"
        html += f"<div class='tiro-marcador' style='left: {tiro}%;'></div>"
    html += "<div class='ruleta-container'>"
    for i, cant in enumerate(casilleros):
        if cant > 0: html += f"<div class='ruleta-porcion color-{i%10}' style='width: {cant}%;'>I{i}</div>"
    html += "</div></div>"
    return html

def _html_torneo_barras(competidores, ganador, fitness_array, titulo):
    html = f"<div style='display: flex; flex-direction: column; align-items: center; background: #f8f9fa; padding: 10px; border-radius: 6px; border: 1px solid #e0e0e0;'>"
    html += f"<strong style='margin-bottom: 10px; color: #2c3e50;'>{titulo}</strong>"
    html += "<div class='torneo-chart'>"
    max_fit = max([fitness_array[i] for i in competidores])
    for i in competidores:
        fit_val = fitness_array[i]
        altura = int((fit_val / max_fit) * 60) if max_fit > 0 else 5
        clase_ganador = "winner" if i == ganador else ""
        html += f"<div class='torneo-bar-wrapper'>"
        html += f"<span class='torneo-val'>{fit_val:.3f}</span>"
        html += f"<div class='torneo-bar {clase_ganador}' style='height: {altura}px;'></div>"
        html += f"<span class='torneo-label'>I-{i}</span>"
        html += "</div>"
    html += "</div></div>"
    return html

def generar_reporte_html(historial_reporte, metodo, generaciones, elitismo):
    estado = "ConElitismo" if elitismo else "SinElitismo"
    nombre = f"REPORTE_{metodo}_{generaciones}gen_{estado}.html"
    os.makedirs("graficos_resultados", exist_ok=True)
    
    html_content = ""
    for gen_data in historial_reporte:
        clase_activa = "active-tab" if gen_data['gen'] == 1 else ""
        html = f"<div id='gen-{gen_data['gen']}' class='tab {clase_activa}'><h2>Generación {gen_data['gen']}</h2>"
        
        html += "<h3>Estado de la Población</h3><table><tr><th>ID</th><th>Cromosoma</th><th>Dec.</th><th>Objetivo</th><th>Fitness</th></tr>"
        for i in range(POBLACION_TAM):
            crom = _html_cromosoma(gen_data['poblacion'][i])
            html += f"<tr><td>{i}</td><td>{crom}</td><td>{binario_a_decimal(gen_data['poblacion'][i])}</td><td>{gen_data['objetivos'][i]:.6f}</td><td>{gen_data['fitness'][i]:.4f}</td></tr>"
        html += "</table>"

        html += "<div class='seccion'><h3>Reproducción</h3>"
        
        # --- RENDERIZADO VISUAL DE ELITISMO ---
        if elitismo:
            # Buscamos los IDs originales de los individuos elite
            elite_indices = []
            for e in gen_data['elite']:
                for idx, ind in enumerate(gen_data['poblacion']):
                    if e == ind and idx not in elite_indices:
                        elite_indices.append(idx)
                        break
            
            html += "<div class='reproduccion-par' style='background: #eafaf1; border-color: #a9dfbf;'>"
            html += "<h4 style='color: #1e8449; margin-top: 0;'>🏅 Selección por Elitismo</h4>"
            html += "<p>Evaluación de toda la población para preservar a los mejores:</p>"
            html += "<div class='elitismo-container'>"
            for i in range(POBLACION_TAM):
                clase = "elite" if i in elite_indices else ""
                html += f"<div class='elitismo-card {clase}'>Ind {i}<br><small>Fit: {gen_data['fitness'][i]:.3f}</small></div>"
            html += "</div>"
            
            nombres_elite = " y ".join([f"Ind {i}" for i in elite_indices])
            html += f"<p>Por elitismo se seleccionaron el <strong>{nombres_elite}</strong>. Estos pasan intactos a la siguiente generación:</p>"
            for idx in elite_indices:
                html += f"<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 5px;'><strong style='width: 45px;'>Ind {idx}:</strong>"
                html += _html_cromosoma(gen_data['poblacion'][idx])
                html += "</div>"
            html += "</div>"

        # --- RENDERIZADO DEL MÉTODO (RULETA O TORNEO) ---
        if metodo == "Ruleta":
            html += "<h4>Distribución de la Ruleta y Tiros</h4>"
            html += _html_barra_ruleta(gen_data['casilleros'], gen_data['tiros'])

        pares_contador = 1
        for cruce in gen_data['cruces']:
            html += f"<div class='reproduccion-par'><h4>Par {pares_contador}</h4>"
            
            if metodo == "Ruleta":
                html += f"<p>Padre 1: Ind {cruce['idx1']} (Tiro: {cruce['t1']}) | Padre 2: Ind {cruce['idx2']} (Tiro: {cruce['t2']})</p>"
            else:
                html += "<div class='torneo-contenedor'>"
                html += _html_torneo_barras(cruce['asp1'], cruce['idx1'], gen_data['fitness'], "Torneo 1")
                html += _html_torneo_barras(cruce['asp2'], cruce['idx2'], gen_data['fitness'], "Torneo 2")
                html += "</div>"
            
            html += "<p><strong>Padres seleccionados:</strong></p>"
            html += _html_cromosoma(cruce['p1'], punto_corte=cruce['punto'])
            html += _html_cromosoma(cruce['p2'], punto_corte=cruce['punto'])
            
            if cruce['punto']: html += f"<p><strong>Cruce realizado en el punto: {cruce['punto']}</strong></p>"
            else: html += "<p><strong>Sin cruce (clones)</strong></p>"

            html += "<p><strong>Hijos resultantes:</strong></p>"
            html += _html_cromosoma(cruce['h1'], pos_mutacion=cruce['m1'])
            if cruce['m1'] is not None: html += f"<p style='margin-top:0; font-size: 12px; color: #c0392b;'>H1 mutó en bit {cruce['m1']}</p>"
            html += _html_cromosoma(cruce['h2'], pos_mutacion=cruce['m2'])
            if cruce['m2'] is not None: html += f"<p style='margin-top:0; font-size: 12px; color: #c0392b;'>H2 mutó en bit {cruce['m2']}</p>"
            
            html += "</div>"
            pares_contador += 1
            
        html += "</div></div>"
        html_content += html

    # Plantilla Base con el CSS inyectado
    plantilla = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Reporte {metodo}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; display: flex; margin: 0; height: 100vh; background: #f4f7f6; color: #333; }}
        #sidebar {{ width: 250px; background: #2c3e50; color: white; overflow-y: auto; padding: 10px; }}
        #sidebar button {{ display: block; width: 100%; padding: 10px; margin-bottom: 5px; background: #34495e; color: white; border: none; cursor: pointer; text-align: left; }}
        #sidebar button.active-btn {{ background: #16a085; border-left: 4px solid #f1c40f; font-weight: bold; }}
        #sidebar button:hover {{ background: #1abc9c; }}
        #content {{ flex-grow: 1; padding: 30px; overflow-y: auto; }}
        .tab {{ display: none; background: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        .active-tab {{ display: block; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #e0e0e0; padding: 10px; text-align: left; }}
        th {{ background: #f8f9fa; }}
        
        /* CSS Cromosomas */
        .cromosoma {{ display: flex; margin-bottom: 5px; }}
        .bit {{ width: 20px; height: 25px; border: 1px solid #ccc; display: flex; justify-content: center; align-items: center; font-family: monospace; font-size: 14px; background: #fff; }}
        .bit.corte {{ border-left: 3px solid #3498db; margin-left: 2px; }}
        .bit.mutado {{ background: #f1c40f; color: #c0392b; font-weight: bold; border-color: #e67e22; }}
        
        /* CSS Ruleta */
        .ruleta-container {{ width: 100%; height: 30px; background: #ecf0f1; display: flex; border: 1px solid #bdc3c7; border-radius: 4px; overflow: hidden; }}
        .ruleta-porcion {{ height: 100%; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px; overflow: hidden; }}
        .tiro-marcador {{ position: absolute; top: -10px; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 10px solid #e74c3c; z-index: 10; }}
        .tiro-label {{ position: absolute; top: -25px; font-size: 10px; color: #c0392b; transform: translateX(-50%); font-weight: bold; }}
        
        /* CSS Torneo de Barras */
        .torneo-contenedor {{ display: flex; gap: 30px; margin-bottom: 15px; }}
        .torneo-chart {{ display: flex; align-items: flex-end; gap: 15px; height: 80px; padding-top: 5px; }}
        .torneo-bar-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%; }}
        .torneo-bar {{ width: 25px; background: #bdc3c7; border-radius: 3px 3px 0 0; transition: height 0.3s; }}
        .torneo-bar.winner {{ background: #2ecc71; box-shadow: 0 0 5px rgba(46,204,113,0.6); }}
        .torneo-val {{ font-size: 10px; color: #7f8c8d; margin-bottom: 3px; }}
        .torneo-label {{ font-size: 11px; font-weight: bold; margin-top: 5px; color: #34495e; }}

        /* CSS Elitismo */
        .elitismo-container {{ display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; justify-content: space-between; }}
        .elitismo-card {{ padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px; background: #ecf0f1; text-align: center; font-size: 11px; flex: 1; min-width: 40px; }}
        .elitismo-card.elite {{ background: #2ecc71; color: white; border-color: #27ae60; font-weight: bold; box-shadow: 0 0 5px rgba(46,204,113,0.5); transform: scale(1.05); }}

        .seccion {{ margin-top: 25px; border-left: 4px solid #3498db; padding-left: 15px; background: #fcfcfc; padding: 15px; border-radius: 0 4px 4px 0; }}
        .reproduccion-par {{ background: #fff; border: 1px solid #eee; padding: 20px; margin-bottom: 20px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        
        .color-0 {{ background: #1abc9c; }} .color-1 {{ background: #2ecc71; }} .color-2 {{ background: #3498db; }}
        .color-3 {{ background: #9b59b6; }} .color-4 {{ background: #34495e; }} .color-5 {{ background: #f1c40f; color: #333; }}
        .color-6 {{ background: #e67e22; }} .color-7 {{ background: #e74c3c; }} .color-8 {{ background: #95a5a6; }} .color-9 {{ background: #7f8c8d; }}
    </style>
    <script>
        function showGen(n) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active-tab'));
            document.getElementById('gen-'+n).classList.add('active-tab');
            document.querySelectorAll('#sidebar button').forEach(b => b.classList.remove('active-btn'));
            document.getElementById('btn-gen-'+n).classList.add('active-btn');
        }}
    </script>
    </head>
    <body>
        <div id="sidebar"><h3>Generaciones</h3>{"".join([f"<button id='btn-gen-{i}' onclick='showGen({i})' class='{'active-btn' if i==1 else ''}'>Gen {i}</button>" for i in range(1, generaciones+1)])}</div>
        <div id="content"><h1>Reporte Analítico: {metodo} ({estado})</h1>{html_content}</div>
    </body></html>
    """
    with open(f"graficos_resultados/{nombre}", "w", encoding="utf-8") as f:
        f.write(plantilla)