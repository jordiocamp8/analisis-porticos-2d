# rigidez.py
import numpy as np

def matriz_rigidez_barra_2D(x1, y1, x2, y2, E, A):
    """
    Calcula la matriz de rigidez local de una barra 2D en coordenadas globales.
    Entradas:
        x1, y1, x2, y2: coordenadas de los nodos (mm)
        E: módulo de elasticidad (MPa)
        A: área (cm²)
    Salida:
        k_global: matriz 4x4
        L: longitud de la barra
    """
    # Convertir unidades: A de cm² a mm², E de MPa a N/mm² (no cambia)
    A_mm2 = A * 100  # 1 cm² = 100 mm²

    # Longitud
    dx = x2 - x1
    dy = y2 - y1
    L = (dx**2 + dy**2)**0.5

    # Coseno directores
    c = dx / L
    s = dy / L

    # Matriz de rigidez local en coordenadas globales (4x4)
    k = (E * A_mm2 / L) * np.array([
        [ c*c,  c*s, -c*c, -c*s],
        [ c*s,  s*s, -c*s, -s*s],
        [-c*c, -c*s,  c*c,  c*s],
        [-c*s, -s*s,  c*s,  s*s]
    ])

    return k, L
