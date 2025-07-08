import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from ensamblador import ensamblar_matriz_global
from resolucion import resolver_sistema

st.set_page_config(page_title="Análisis de Pórticos 2D", layout="centered")
st.title("🧱 Análisis de Pórticos 2D")
st.write("Este sistema calcula desplazamientos y reacciones dadas las propiedades del pórtico.")

# NODOS
st.header("🔹 Nodos")
num_nodos = st.number_input("Cantidad de nodos", min_value=2, max_value=10, value=3)
nodos = {}
for i in range(1, num_nodos + 1):
    x = st.number_input(f"Nodo {i} - X (mm)", key=f"x{i}")
    y = st.number_input(f"Nodo {i} - Y (mm)", key=f"y{i}")
    nodos[i] = [x, y]

# Validación de nodos duplicados
if len(set(map(tuple, nodos.values()))) != len(nodos):
    st.warning("⚠️ Hay nodos duplicados con las mismas coordenadas. Verifica las entradas.")

# BARRAS
st.header("🔸 Barras")
num_barras = st.number_input("Cantidad de barras", min_value=1, max_value=15, value=2)
barras = {}
for i in range(1, num_barras + 1):
    n1 = st.number_input(f"Barra {i} - Nodo inicial", min_value=1, max_value=num_nodos, key=f"n1_{i}")
    n2 = st.number_input(f"Barra {i} - Nodo final", min_value=1, max_value=num_nodos, key=f"n2_{i}")
    E = st.number_input(f"Barra {i} - Módulo E (MPa)", value=210000.0, key=f"E_{i}")
    A = st.number_input(f"Barra {i} - Área (cm²)", value=30.0, key=f"A_{i}")
    I = st.number_input(f"Barra {i} - Inercia (cm⁴)", value=500.0, key=f"I_{i}")

    tipo_carga = st.selectbox(f"Tipo de carga en Barra {i}", options=["Ninguna", "Uniforme", "Triangular", "Inclinada"], key=f"tipo_carga_{i}")
    carga = None
    if tipo_carga == "Uniforme":
        w = st.number_input(f"Barra {i} - Carga uniforme (kN/m)", key=f"w_{i}")
        carga = {"tipo": "uniforme", "valor": w}
    elif tipo_carga == "Triangular":
        w_max = st.number_input(f"Barra {i} - Carga triangular máx (kN/m)", key=f"w_tri_{i}")
        carga = {"tipo": "triangular", "valor": w_max}
    elif tipo_carga == "Inclinada":
        mag = st.number_input(f"Barra {i} - Magnitud (kN/m)", key=f"mag_{i}")
        ang = st.number_input(f"Barra {i} - Ángulo (°)", key=f"ang_{i}")
        carga = {"tipo": "inclinada", "magnitud": mag, "angulo": ang}

    barras[i] = {
        "nodos": [n1, n2],
        "E": E,
        "A": A,
        "I": I,
        "carga": carga
    }

# Validación de barras duplicadas
pares_barras = [tuple(sorted(datos["nodos"])) for datos in barras.values()]
if len(set(pares_barras)) != len(pares_barras):
    st.warning("⚠️ Hay barras duplicadas que conectan los mismos nodos.")

# RESTRICCIONES
st.header("🛑 Restricciones (apoyos)")
restricciones = {}
for i in range(1, num_nodos + 1):
    col1, col2, col3 = st.columns(3)
    with col1:
        r_x = st.checkbox(f"Nodo {i} restringido en X", key=f"rx_{i}")
    with col2:
        r_y = st.checkbox(f"Nodo {i} restringido en Y", key=f"ry_{i}")
    with col3:
        r_rot = st.checkbox(f"Nodo {i} restringido en Rotación", key=f"rrot_{i}")
    restricciones[i] = [int(r_x), int(r_y), int(r_rot)]

# CARGAS NODALES
st.header("📥 Cargas nodales (kN / kN·mm)")
cargas = {}
for i in range(1, num_nodos + 1):
    fx = st.number_input(f"Nodo {i} - Carga en X", value=0.0, key=f"fx_{i}")
    fy = st.number_input(f"Nodo {i} - Carga en Y", value=0.0, key=f"fy_{i}")
    mz = st.number_input(f"Nodo {i} - Momento (kN·mm)", value=0.0, key=f"mz_{i}")
    cargas[i] = [fx, fy, mz]

# EJECUCIÓN
st.header("🛠️ Ejecución")
if st.button("Calcular"):
    estructura = {
        "nodos": nodos,
        "barras": barras,
        "restricciones": restricciones,
        "cargas": cargas
    }

    try:
        K_global, F_global = ensamblar_matriz_global(estructura)
        estructura["fuerzas"] = F_global
        U, R = resolver_sistema(K_global, estructura)

        st.subheader("📀 Desplazamientos nodales (mm, rad)")
        st.code(np.round(U, 4))

        st.subheader("📌 Reacciones en apoyos (kN, kN·mm)")
        st.code(np.round(R, 4))

        # GRAFICO: estructura y deformada
        st.subheader("📊 Estructura original y deformada")
        fig, ax = plt.subplots()
        escala = 100  # Escala para amplificar deformada

        for datos_barra in estructura["barras"].values():
            n1, n2 = datos_barra["nodos"]
            x1, y1 = estructura["nodos"][n1]
            x2, y2 = estructura["nodos"][n2]

            u1 = U[3 * (n1 - 1)]
            v1 = U[3 * (n1 - 1) + 1]
            u2 = U[3 * (n2 - 1)]
            v2 = U[3 * (n2 - 1) + 1]

            ax.plot([x1, x2], [y1, y2], 'k--')
            ax.plot([x1 + u1 * escala, x2 + u2 * escala],
                    [y1 + v1 * escala, y2 + v2 * escala], 'b-')

        ax.set_aspect('equal')
        ax.set_title("Vista estructural")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.grid(True)
        st.pyplot(fig)

        # GRAFICO: Diagramas de momento y cortante
        st.subheader("📉 Diagramas por barra")
        for i, datos_barra in estructura["barras"].items():
            n1, n2 = datos_barra["nodos"]
            x1, y1 = estructura["nodos"][n1]
            x2, y2 = estructura["nodos"][n2]
            L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            v1 = U[3*(n1-1)+1]
            v2 = U[3*(n2-1)+1]
            r1 = U[3*(n1-1)+2]
            r2 = U[3*(n2-1)+2]

            x_vals = np.linspace(0, L, 50)
            V = np.full_like(x_vals, np.nan)
            M = np.full_like(x_vals, np.nan)

            for j, x in enumerate(x_vals):
                V[j] = (12/L**3)*(v2 - v1)*x - (6/L**2)*(r1 + r2)
                M[j] = (6/L**2)*(v2 - v1)*x**2 + (2/L)*(r1*(1 - x/L) + r2*x/L)

            fig_v, ax_v = plt.subplots()
            ax_v.plot(x_vals, V, 'r-')
            ax_v.set_title(f"Cortante - Barra {i}")
            ax_v.set_xlabel("Longitud (mm)")
            ax_v.set_ylabel("V (kN)")
            ax_v.grid(True)
            st.pyplot(fig_v)

            fig_m, ax_m = plt.subplots()
            ax_m.plot(x_vals, M, 'g-')
            ax_m.set_title(f"Momento flector - Barra {i}")
            ax_m.set_xlabel("Longitud (mm)")
            ax_m.set_ylabel("M (kN·mm)")
            ax_m.grid(True)
            st.pyplot(fig_m)

    except Exception as e:
        st.error(f"❌ Ocurrió un error: {e}")
