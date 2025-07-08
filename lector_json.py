# lector_json.py
import json

def cargar_estructura(ruta):
    with open(ruta, "r") as archivo:
        datos = json.load(archivo)
    return datos

if __name__ == "__main__":
    estructura = cargar_estructura("estructura.json")

    print("📍 Nodos:")
    for id_nodo, coord in estructura["nodos"].items():
        print(f" Nodo {id_nodo}: Coordenadas = {coord}")

    print("\n🔩 Barras:")
    for id_barra, datos in estructura["barras"].items():
        n1, n2 = datos["nodos"]
        E = datos["E"]
        A = datos["A"]
        I = datos.get("I", "No definido")
        carga = datos.get("carga", "Ninguna")

        print(f" Barra {id_barra}: nodos {n1}-{n2}, E={E} MPa, A={A} cm², I={I} cm⁴, Carga={carga}")

        # Verificación de nodos existentes
        if str(n1) not in estructura["nodos"] or str(n2) not in estructura["nodos"]:
            print(f" ⚠️ Barra {id_barra} hace referencia a nodos inexistentes.")

    if "restricciones" in estructura:
        print("\n🛑 Restricciones:")
        for nodo, restr in estructura["restricciones"].items():
            print(f" Nodo {nodo}: Restringido en X={restr[0]}, Y={restr[1]}, Rotación={restr[2]}")

    if "cargas" in estructura:
        print("\n📥 Cargas nodales:")
        for nodo, carga in estructura["cargas"].items():
            print(f" Nodo {nodo}: FX={carga[0]} kN, FY={carga[1]} kN, MZ={carga[2]} kN·mm")
