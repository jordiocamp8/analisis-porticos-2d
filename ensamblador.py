import numpy as np

def ensamblar_matriz_global(estructura):
    nodos = estructura["nodos"]
    barras = estructura["barras"]
    n_nodos = len(nodos)
    n_grados_libertad = 3 * n_nodos

    K_global = np.zeros((n_grados_libertad, n_grados_libertad))
    F_global = np.zeros(n_grados_libertad)

    for datos_barra in barras.values():
        n1, n2 = datos_barra["nodos"]
        x1, y1 = nodos[n1]
        x2, y2 = nodos[n2]

        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        C = (x2 - x1) / L
        S = (y2 - y1) / L

        E = datos_barra["E"]
        A = datos_barra["A"]
        I = datos_barra.get("I", 1.0)  # Valor por defecto

        # MATRIZ LOCAL DE RIGIDEZ PARA VIGA 2D CON 3 GDL POR NODO
        k = E / L
        k_local = k * np.array([
            [ A*C**2 + 12*I*S**2/L**2, (A - 12*I/L**2)*C*S, -6*I*S/L, -A*C**2 - 12*I*S**2/L**2, -(A - 12*I/L**2)*C*S, -6*I*S/L ],
            [ (A - 12*I/L**2)*C*S, A*S**2 + 12*I*C**2/L**2, 6*I*C/L, -(A - 12*I/L**2)*C*S, -A*S**2 - 12*I*C**2/L**2, 6*I*C/L ],
            [ -6*I*S/L, 6*I*C/L, 4*I, 6*I*S/L, -6*I*C/L, 2*I ],
            [ -A*C**2 - 12*I*S**2/L**2, -(A - 12*I/L**2)*C*S, 6*I*S/L, A*C**2 + 12*I*S**2/L**2, (A - 12*I/L**2)*C*S, 6*I*S/L ],
            [ -(A - 12*I/L**2)*C*S, -A*S**2 - 12*I*C**2/L**2, -6*I*C/L, (A - 12*I/L**2)*C*S, A*S**2 + 12*I*C**2/L**2, -6*I*C/L ],
            [ -6*I*S/L, 6*I*C/L, 2*I, 6*I*S/L, -6*I*C/L, 4*I ]
        ])

        # GRADOS DE LIBERTAD GLOBALES
        dofs = [3*(n1-1), 3*(n1-1)+1, 3*(n1-1)+2,
                3*(n2-1), 3*(n2-1)+1, 3*(n2-1)+2]

        # ENSAMBLA MATRIZ LOCAL EN LA GLOBAL
        for i in range(6):
            for j in range(6):
                K_global[dofs[i], dofs[j]] += k_local[i, j]

        # CARGAS DISTRIBUIDAS APLICADAS COMO FUERZAS NODALES
        carga = datos_barra.get("carga")
        f_local = np.zeros(6)

        if carga:
            if carga["tipo"] == "uniforme":
                w = carga["valor"]
                f_local = np.array([
                    0, -w*L/2, -w*L**2/12,
                    0, -w*L/2, w*L**2/12
                ])
            elif carga["tipo"] == "triangular":
                w = carga["valor"]
                f_local = np.array([
                    0, -w*L/3, -w*L**2/20,
                    0, -2*w*L/3, w*L**2/30
                ])
            elif carga["tipo"] == "inclinada":
                mag = carga["magnitud"]
                ang = np.radians(carga["angulo"])
                wx = mag * np.cos(ang)
                wy = mag * np.sin(ang)

                f_x = np.array([
                    wx*L/2, 0, 0,
                    wx*L/2, 0, 0
                ])
                f_y = np.array([
                    0, -wy*L/2, -wy*L**2/12,
                    0, -wy*L/2, wy*L**2/12
                ])
                f_local = f_x + f_y

        # SUMAR CARGAS A FUERZA GLOBAL
        for i in range(6):
            F_global[dofs[i]] += f_local[i]

    estructura["fuerzas"] = F_global
    return K_global, F_global
