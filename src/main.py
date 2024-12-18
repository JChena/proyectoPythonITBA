
import streamlit as st


pages = {
    "Actualizar Datos": [
        st.Page("../src/pages/ppal.py", title="Actualizar datos",
                icon=":material/home:"),
    ],
    "Mostrar datos": [
        st.Page("../src/pages/datos_BD.py", title="Mostrar Resumen",
                icon=":material/database:"),
        st.Page("../src/pages/graficas.py", title="Graficar ticker",
                icon=":material/monitoring:"),
    ],
}

pg = st.navigation(pages)
pg.run()

st.logo("static/logo3.png", size="large")
