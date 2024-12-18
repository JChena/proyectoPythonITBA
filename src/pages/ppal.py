from datetime import datetime, timedelta
import sqlite3
import requests
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st


class DatabaseHandler:
    def __init__(self, db_path):
        """Inicializa con la ruta a la BD."""
        self.db_path = db_path

    def _connect(self):
        """Establece una conexion con la BD."""
        return sqlite3.connect(self.db_path)

    def guardar_datos(self, ticker, resultados):
        """Almacena los datos obtenidos en la BD si es que los datos no existen. Si los datos existen no los pisa."""
        conexion = self._connect()
        cursor = conexion.cursor()

        for dato in resultados:
            date = datetime.utcfromtimestamp(
                dato['t'] / 1000).strftime('%Y-%m-%d')
            volume = dato['v']
            vwap = dato['vw']
            open_price = dato['o']
            close_price = dato['c']
            high = dato['h']
            low = dato['l']
            transactions = dato['n']

            # Verifica si el dato ya esta almacenado.
            cursor.execute('''
                SELECT * FROM financial_data_polygon
                WHERE ticker = ? AND date = ?
            ''', (ticker, date))

            existing_record = cursor.fetchone()

            # Si el dato no esta en la BD, los inserta.
            if not existing_record:
                cursor.execute('''
                    INSERT INTO financial_data_polygon (ticker, date, volume, vwap, open, close, high, low, transactions)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (ticker, date, volume, vwap, open_price, close_price, high, low, transactions))

        conexion.commit()
        conexion.close()

    def get_tickers(self):
        """Muestra los tickers existente para que el usuario elija posteriormente."""
        engine = create_engine(f'sqlite:///{self.db_path}')
        tickers_df = pd.read_sql(
            "SELECT DISTINCT ticker FROM maestra_tickers ORDER BY ticker", engine)
        return tickers_df['ticker'].tolist()


class APIClient:
    def __init__(self, api_key):
        """Inicializa el cliente con su api key."""
        self.api_key = api_key

    def get_data(self, ticker, fecha_inicio, fecha_fin):
        """Solicita la informacion del ticker a  Polygon API."""
        url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio}/{fecha_fin}'
        params = {"sort": "asc", "apiKey": self.api_key}
        response = requests.get(url, params=params, timeout=15)

        if response.status_code == 200:
            return response.json()
        else:
            return None


class DataUpdater:
    # Tiene la logica principal de la aplicacion -coordina la validacion de datos, la solicitud a la API y el almacenamiento de #la rta
    def __init__(self, db_handler, api_client):
        """Se inicializa creando instancias de las clases DatabaseHandler y APIClient."""
        self.db_handler = db_handler
        self.api_client = api_client

    def validar_fecha(self, fecha_input):
        """Convierte fechas datetime a formato string requerido por la API"""
        return fecha_input.strftime("%Y-%m-%d")

    def actualizar_datos(self, ticker, fecha_inicio, fecha_fin):
        """Obtiene los datos de la API y los guarda en la BD."""

        # Convierte fechas a formato string
        fecha_inicio_str = self.validar_fecha(fecha_inicio)
        fecha_fin_str = self.validar_fecha(fecha_fin)

        # Solicitud get a la API
        data = self.api_client.get_data(
            ticker, fecha_inicio_str, fecha_fin_str)

        if data and data.get('results'):
            self.db_handler.guardar_datos(ticker, data['results'])
            st.balloons()
            st.success(
                "Datos obtenidos correctamente y guardados en la base de datos.")
        else:
            st.warning(
                f"No se encontraron datos para el rango {fecha_inicio_str} a {fecha_fin_str}.")


# Interface Streamlit

st.title("Data Shares")
st.write("Para actualizar tickers, ingresa los siguientes datos: ")

# Inicializa objetos DataHandler y API Client
db_path = "finanzas_P.db"
api_key = "7EuDFFydcjhpG3G0JaoJmBUgpNDOZnp8"
db_handler = DatabaseHandler(db_path)
api_client = APIClient(api_key)

# Inicializa el objeto DataUpdater
data_updater = DataUpdater(db_handler, api_client)

# Posibles tickers para seleccionar
tickers_existentes = db_handler.get_tickers()

# Inputs del usuario
ticker = st.selectbox("Seleccione un ticker de interes",
                      tickers_existentes, index=None, placeholder="Ver opciones")

fecha_inicio = st.date_input(
    "Ingrese la fecha de inicio", value=None, max_value=datetime.now())

solo_un_dia = st.checkbox("Solo cotizaciones de un dia.")

if solo_un_dia:
    fecha_fin = fecha_inicio
    st.text(f"Buscar cotizaciones para el dia: {fecha_fin}")
else:
    fecha_fin = st.date_input(
        "Ingrese la fecha de fin", value=None, max_value=datetime.now())

# Boton para iniciar la actualizacion de datos seleccionada por el usuario
actualizar = st.button(label="Actualizar")

if actualizar:
    # Llama al metodo y almacena la informacion en la BD
    data_updater.actualizar_datos(ticker, fecha_inicio, fecha_fin)
