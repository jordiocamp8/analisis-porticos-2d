import numpy as np

def resolver_sistema(K_global, estructura):
    F = estructura["fuerzas"]
    restricciones = estructura["restricciones"]
    n_nodos = len(estructura["nodos"])
    n_dof = 3 * n_nodos

    # Generar índices de grados de libertad restringidos y libres
    fijas = []
    for nodo, restr in restricciones.items():
        base = 3 * (int(nodo) - 1)
        if restr[0]:  # restricción en X
            fijas.append(base)
        if restr[1]:  # restricción en Y
            fijas.append(base + 1)
        if restr[2]:  # restricción en Rotación
            fijas.append(base + 2)

    libres = [i for i in range(n_dof) if i not in fijas]

    if len(libres) == 0:
        raise ValueError("No hay grados de libertad libres. Revisa las restricciones.")

    # Submatrices y vectores
    try:
        K_ll = K_global[np.ix_(libres, libres)]
        K_fl = K_global[np.ix_(fijas, libres)]
        F_l = F[libres]
        F_f = F[fijas]

        # Resolver sistema
        U = np.zeros(n_dof)
        R = np.zeros(n_dof)
        U_l = np.linalg.solve(K_ll, F_l)
        U[libres] = U_l
        R[fijas] = K_fl @ U_l - F_f

        return U, R

    except np.linalg.LinAlgError:
        raise ValueError("Error al resolver el sistema. La matriz es singular o está mal definida.")
