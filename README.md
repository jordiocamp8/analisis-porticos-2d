# 🏗️ Análisis de Pórticos 2D

Esta es una aplicación desarrollada en **Python con Streamlit** para el análisis estructural de pórticos bidimensionales (2D) usando el método de la rigidez.

---

## 🚀 Características

- Carga de nodos y barras desde una interfaz gráfica.
- Visualización de la estructura original y deformada.
- Soporta cargas:
  - Puntuales
  - Distribuidas uniformes
  - Distribuidas triangulares
- Cálculo de desplazamientos nodales.
- Generación de diagramas de **cortante** y **momento flector**.

---

## 🖥️ ¿Cómo usar?

1. Clona el repositorio:

```bash
git clone https://github.com/jordiocamp8/analisis-porticos-2d.git
cd analisis-porticos-2d

Instala las dependencias:
pip install streamlit numpy matplotlib

Ejecuta la aplicación:
streamlit run app_streamlit.py

Estructura del Proyecto
📦 analisis-porticos-2d
 ┣ 📜 app_streamlit.py         → Interfaz gráfica Streamlit
 ┣ 📜 app.py                   → Lógica alternativa (modular)
 ┣ 📜 ensamblador.py           → Ensamble de matrices de rigidez
 ┣ 📜 lector_json.py           → Carga de estructura desde JSON
 ┣ 📜 resolucion.py            → Resolución del sistema de ecuaciones
 ┣ 📜 rigidez.py               → Cálculo de rigidez local
 ┣ 📜 estructura.json          → Datos de ejemplo
 ┗ 📜 README.md                → Este archivo


🛠️ Autor
✍️ Jordi Ocampo R.

💻 Repositorio: github.com/jordiocamp8/analisis-porticos-2d

📌 Licencia
Este proyecto está bajo la licencia MIT. ¡Úsalo libremente y contribuye si quieres!
UNIVERSIDAD TECNICA PARTICULAR DE LOJA
ING.CIVIL
