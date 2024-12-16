from datetime import datetime, timedelta
import sqlite3
import requests
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
import streamlit as st


def validar_fecha(fecha_input):
    '''Funcion para pasar las fechas a string tal como requiere la API'''
    fecha_str = fecha_input.strftime("%Y-%m-%d")
    return fecha_str


def guardar_datos_en_bd(ticker, resultados):
    '''Funcion que almacena en la base de datos la cotizacion del ticker seleccionado'''
    conexion = sqlite3.connect("finanzas_P.db")
    cursor = conexion.cursor()

    for dato in resultados:
        date = datetime.utcfromtimestamp(
            # Convertir timestamp a fecha
            dato['t'] / 1000).strftime('%Y-%m-%d')
        volume = dato['v']
        vwap = dato['vw']
        open_price = dato['o']
        close_price = dato['c']
        high = dato['h']
        low = dato['l']
        transactions = dato['n']

        # Verificar si el registro existe:
        cursor.execute('''
            SELECT * FROM financial_data_polygon
            WHERE ticker = ? AND date = ?
        ''', (ticker, date))

        existing_record = cursor.fetchone()

        if not existing_record:
            # Si el registro no existe, lo inserta en la BD

            cursor.execute('''
            INSERT INTO financial_data_polygon (ticker, date, volume, vwap, open, close, high, low, transactions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (ticker, date, volume, vwap, open_price, close_price, high, low, transactions))

    conexion.commit()
    conexion.close()

# Función para hacer la solicitud de datos a la API


# def solicitud_de_datos(ticker, fecha_inicio, fecha_fin):
    # Conexión a la base de datos
    # conexion = sqlite3.connect("src/finanzas_P.db")
    # cursor = conexion.cursor()

    # Verificar los rangos existentes en la base de datos para el ticker
    # consulta = f"""
    # SELECT MIN(date), MAX(date) FROM financial_data_polygon WHERE ticker = '{ticker}'
    # """
    # cursor.execute(consulta, (ticker,))
    # resultado = cursor.fetchone()
    # conexion.close()

    # engine = create_engine(
    #     'sqlite:////Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/finanzas_P.db')
    # metadata = MetaData()
    # maestra = Table('maestra_tickers', metadata, autoload_with=engine)
    # st.write(repr(maestra))

    # resultado = pd.read_sql(consulta, engine)

    # st.dataframe(resultado)

    # if not resultado.empty:
    #     # Rango existente en la base de datos
    #     fecha_guardada_inicio, fecha_guardada_fin = resultado
    #     st.write(fecha_guardada_inicio)
    #     st.write(fecha_guardada_fin)

    #     # Ajustar las fechas para pedir solo los datos faltantes
    #     if fecha_inicio < fecha_guardada_inicio:
    #         rango_inicio = fecha_inicio
    #         rango_fin = (datetime.strptime(fecha_guardada_inicio, "%Y-%m-%d") -
    #                      timedelta(days=1)).strftime("%Y-%m-%d")
    #     else:
    #         rango_inicio, rango_fin = None, None

    #     if fecha_fin > fecha_guardada_fin:
    #         rango_inicio_extra = (datetime.strptime(
    #             fecha_guardada_fin, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    #         rango_fin_extra = fecha_fin
    #     else:
    #         rango_inicio_extra, rango_fin_extra = None, None

    #     # Llamar a la API para los rangos faltantes
    #     if rango_inicio and rango_fin:
    #         # st.write(f'''Pidiendo datos para el ticker {ticker} desde {rango_inicio} hasta {rango_fin}...''')
    #         llamar_api_y_guardar(ticker, rango_inicio, rango_fin)

    #     if rango_inicio_extra and rango_fin_extra:
    #         # st.write(f'''Pidiendo datos para el ticker {ticker} desde {rango_inicio_extra} hasta {rango_fin_extra}...''')
    #         llamar_api_y_guardar(ticker, rango_inicio_extra, rango_fin_extra)

    # else:
    #     # No hay datos en la base de datos, pedir todo el rango solicitado
    #     print(f"Pidiendo datos desde {fecha_inicio} hasta {fecha_fin}...")
    #     llamar_api_y_guardar(ticker, fecha_inicio, fecha_fin)
    #     st.balloons()
    #     st.success(
    #         "Datos obtenidos correctamente y guardados en la base de datos.")


def llamar_api_y_guardar(ticker, fecha_inicio, fecha_fin):
    # Función separada para manejar la solicitud a la API y guardar los datos
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio}/{fecha_fin}'
    api_key = "7EuDFFydcjhpG3G0JaoJmBUgpNDOZnp8"
    params = {"sort": "asc", "apiKey": api_key}

    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 200:
        datos = response.json()
        if datos.get('results'):
            guardar_datos_en_bd(ticker, datos['results'])
            st.balloons()
            st.success(
                "Datos obtenidos correctamente y guardados en la base de datos.")
        else:
            st.warning(
                f"No se encontraron datos para el rango {fecha_inicio} a {fecha_fin}.")
    else:
        st.error(
            f"Error al pedir datos. Código de estado: {response.status_code}")


# def solicitud_de_datos(ticker, fecha_inicio, fecha_fin):
#     '''Funcion que hace el request de cotizaciones a la AIP'''
#     # Construir la URL
#     url = f"https://api.polygon.io/v2/aggs/ticker/{
#         ticker}/range/1/day/{fecha_inicio}/{fecha_fin}"
#     api_key = "7EuDFFydcjhpG3G0JaoJmBUgpNDOZnp8"
#     params = {"sort": "asc", "apiKey": api_key}

#     # Solicitud GET a la API
#     response = requests.get(url, params=params, timeout=15)

#     # Verificamos el código de estado
#     if response.status_code == 200:

#         datos = response.json()  # Parseamos los datos JSON de la respuesta
#         if datos.get('results'):
#             st.balloons()
#             st.success(
#                 "Datos obtenidos correctamente y guardados en la base de datos.")
#             guardar_datos_en_bd(ticker, datos['results'])
#         else:
#             st.warning(
#                 "No se encontraron resultados para el rango de fechas proporcionado.")
#     else:
#         # En caso de error, mostramos más detalles
#         st.error(
#             f"Hubo un error al pedir los datos. Status code: {response.status_code}")
#         # Mostramos el mensaje de error recibido de la API
#         st.warning("Respuesta de error:", response.text)


st.title("Data Shares")

st.write("Para actualizar tickers, ingresa los siguientes datos: ")

# Creo un iterable con los tickers disponibles en la tabla maestra de tickers
engine = create_engine(
    'sqlite:////Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/finanzas_P.db')

tickers_existentes = pd.read_sql(
    "SELECT DISTINCT ticker FROM maestra_tickers ORDER BY ticker", engine)

# Variables para inputs del ususario
ticker = st.selectbox("Seleccione un ticker de interes", tickers_existentes,
                      index=None, placeholder="Ver opciones")

fecha_inicio = st.date_input(
    "Ingrese la fecha de inicio", value=None, max_value=datetime.now())

solo_un_dia = st.checkbox("Solo cotizaciones de un dia.")

if solo_un_dia:
    fecha_fin = fecha_inicio
    st.text(f"Buscar cotizaciones para el dia: {fecha_fin}")
else:
    fecha_fin = st.date_input(
        "Ingrese la fecha de fin", value=None, max_value=datetime.now())

# Boton para iniciar la solicitud del usuario
actualizar = st.button(label="Actualizar")

if actualizar:
    # Pasamos las fechas de datetime object a string para hacer la solicitud a la api correctamente
    fecha1 = validar_fecha(fecha_inicio)
    fecha2 = validar_fecha(fecha_fin)

    # Solicitamos las cotizaciones a la API
    llamar_api_y_guardar(ticker, fecha1, fecha2)
