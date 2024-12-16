from sqlalchemy import create_engine
import sqlite3
import pandas as pd
import streamlit as st

st.title("Datos almacenados")

# engine = create_engine('sqlite:///finanzas_P.db')
engine = create_engine(
    'sqlite:////Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/finanzas_P.db')

consulta = """
    SELECT
        f.ticker,
        m.nombre_compania,
        MIN(f.date) AS fecha_desde,
        MAX(f.date) AS fecha_hasta
    FROM financial_data_polygon f
    LEFT JOIN maestra_tickers m ON f.ticker = m.ticker
    GROUP BY f.ticker
    ORDER BY f.ticker
    """
df = pd.read_sql(consulta, engine)

st.dataframe(df)

st.caption("Las fechas indicadas en la siguiente tabla corresponden a la primera y última con datos de precio para cada Ticker. Podría ocurrir que existan fechas intermedias sin datos. Si se detectan datos faltantes, es necesario pedir la actualización para el rango completo a través de la opción ‘Actualizar Datos’")
