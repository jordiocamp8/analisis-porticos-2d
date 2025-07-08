from lector_json import cargar_estructura
from ensamblador import ensamblar_matriz_global
from resolucion import resolver_sistema
import numpy as np

def main():
    estructura = cargar_estructura("estructura.json")
    K_global = ensamblar_matriz_global(estructura)

    print("Matriz global de rigidez:")
    print(np.round(K_global, 2))
    print()

    U, R = resolver_sistema(K_global, estructura)

    print("Desplazamientos nodales (mm):")
    print(np.round(U, 4))
    print()

    print("Reacciones en apoyos (kN):")
    print(np.round(R, 4))

if __name__ == "__main__":
    main()
