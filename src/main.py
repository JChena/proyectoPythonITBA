import streamlit as st

pages = {
    "Actualizar Datos": [
        st.Page("/Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/src/pages/ppal.py",
                title="Actualizar datos",  icon=":material/home:"),
    ],
    "Mostrar datos": [
        st.Page("/Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/src/pages/datos_BD.py",
                title="Mostrar Resumen",  icon=":material/database:"),
        st.Page("//Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/src/pages/graficas.py",
                title="Graficar ticker", icon=":material/monitoring:"),
    ],
}

pg = st.navigation(pages)
pg.run()

st.logo("static/logo3.png", size="large")
