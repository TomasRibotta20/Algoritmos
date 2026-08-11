import opcion_a as opt_a
import opcion_b as opt_b

def ejecutar_comparativa_elitismo():
    print("--- INICIANDO RULETA CON ELITISMO (100 GEN) ---")
    opt_a.ejecutar_ruleta(100, elitismo=True)
    
    print("\n--- INICIANDO TORNEO CON ELITISMO (100 GEN) ---")
    opt_b.ejecutar_torneo(100, elitismo=True)

if __name__ == "__main__":
    ejecutar_comparativa_elitismo()