from datetime import datetime
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

# Título de la página
st.title("Visualización de datos")

# Conexión a la base de datos
engine = create_engine(
    'sqlite:////Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/finanzas_P.db')

# Columnas para inputs del usuario
col1, col2 = st.columns(2)

with col1:
    # Obtener tickers y nombres de compañías con un JOIN
    query = """
        SELECT DISTINCT f.ticker, m.nombre_compania
        FROM financial_data_polygon f
        LEFT JOIN maestra_tickers m ON f.ticker = m.ticker
        ORDER BY f.ticker
    """

    # Realizar query y guardar el resultado en un dataframe
    tickers_df = pd.read_sql(query, engine)

    # Crear columna combinada para mostrar en el selectbox
    tickers_df['ticker_descripcion'] = tickers_df['ticker'] + \
        " - " + tickers_df['nombre_compania']

    # Lista para mostrar en el selectbox
    opciones = tickers_df['ticker_descripcion'].tolist()

    # Selectbox con ticker y nombre de compañía
    ticker_selecc = st.selectbox(
        "Seleccione un ticker para graficar", opciones, index=0)

    # Extraer solo el ticker seleccionado
    ticker_selecc = ticker_selecc.split(
        " - ")[0]

with col2:
    tipo_grafico = st.radio("Seleccione el tipo de gráfico", [
        "Evolución del precio",
        "Evolución con volumen",
        "Comparativa entre precios (Apertura vs Cierre)",
        "Gráfico de Velas"
    ])

# Botón para generar el gráfico
if st.button("Graficar"):

    # Obtener datos del ticker seleccionado
    consulta = """
        SELECT date, open, close, high, low, volume 
        FROM financial_data_polygon
        WHERE ticker = ?
        ORDER BY date ASC
    """
    df = pd.read_sql(consulta, engine, params=(ticker_selecc,))
    df = df.rename(columns={'date': 'Fecha', 'open': 'Precio apertura', 'close': 'Precio cierre',
                   'high': 'Precio max.', 'low': 'Precio min.', 'volume': 'Volumen'})

    if df.empty:
        st.warning(
            f"No hay datos almacenados para el ticker '{ticker_selecc}'.")
    else:
        # Conversión de fechas
        df['Fecha'] = pd.to_datetime(df['Fecha'])

        # Gráfico seleccionado
        if tipo_grafico == "Evolución del precio":
            plt.figure(figsize=(10, 6))
            plt.plot(df['Fecha'], df['Precio cierre'],
                     label="Precio de Cierre", color="blue")
            plt.xlabel("Fecha")
            plt.ylabel("Precio de Cierre (USD)")
            plt.title(f"Evolución del Precio - {ticker_selecc}")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)

        elif tipo_grafico == "Evolución con volumen":
            fig, ax1 = plt.subplots(figsize=(10, 6))

            ax1.plot(df['Fecha'], df['Precio cierre'],
                     label="Precio de Cierre", color="blue")
            ax1.set_xlabel("Fecha")
            ax1.set_ylabel("Precio de Cierre (USD)", color="blue")
            plt.grid(True)
            ax2 = ax1.twinx()
            ax2.bar(df['Fecha'], df['Volumen'],
                    label="Volumen", color="gray", alpha=0.3)
            ax2.set_ylabel("Volumen", color="gray")

            plt.title(f"Evolución con Volumen - {ticker_selecc}")
            st.pyplot(fig)

        elif tipo_grafico == "Comparativa entre precios (Apertura vs Cierre)":
            plt.figure(figsize=(10, 6))
            plt.plot(df['Fecha'], df['Precio apertura'],
                     label="Precio de Apertura", color="green")
            plt.plot(df['Fecha'], df['Precio cierre'],
                     label="Precio de Cierre", color="blue")
            plt.xlabel("Fecha")
            plt.ylabel("Precio (USD)")
            plt.title(f"Comparativa de Precios - {ticker_selecc}")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)

        elif tipo_grafico == "Gráfico de Velas":
            from mplfinance.original_flavor import candlestick_ohlc
            import matplotlib.dates as mdates

            df_candlestick = df[['Fecha', 'Precio apertura',
                                 'Precio max.', 'Precio min.', 'Precio cierre']].copy()
            df_candlestick['Fecha'] = df_candlestick['Fecha'].map(
                mdates.date2num)

            fig, ax = plt.subplots(figsize=(10, 6))
            candlestick_ohlc(ax, df_candlestick.values,
                             width=0.6, colorup="green", colordown="red")
            ax.xaxis_date()
            ax.set_title(f"Gráfico de Velas - {ticker_selecc}")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Precio (USD)")
            plt.grid(True)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    mostrar_df = st.toggle('Mostrar datos')

    # if mostrar_df:

    #     st.dataframe(df)
