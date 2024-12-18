
from datetime import datetime
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates


class StockDataVisualizer:
    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = create_engine(db_path)
        self.ticker_selecc = None
        self.tipo_grafico = None
        self.df = None

    def load_tickers(self):
        '''Trae los tickers almacenados en BD y los lista para mostrar al usuario'''

        query = """
            SELECT DISTINCT f.ticker, m.nombre_compania
            FROM financial_data_polygon f
            LEFT JOIN maestra_tickers m ON f.ticker = m.ticker
            ORDER BY f.ticker
        """
        tickers_df = pd.read_sql(query, self.engine)
        tickers_df['ticker_descripcion'] = tickers_df['ticker'] + \
            " - " + tickers_df['nombre_compania']
        return tickers_df['ticker_descripcion'].tolist()

    def fetch_data(self, ticker):
        '''Trae los datos almacenados que el usuario solicita para usar en los graficos'''

        consulta = """
            SELECT date, open, close, high, low, volume 
            FROM financial_data_polygon
            WHERE ticker = ?
            ORDER BY date ASC
        """
        self.df = pd.read_sql(consulta, self.engine, params=(ticker,))
        self.df = self.df.rename(columns={'date': 'Fecha', 'open': 'Precio apertura', 'close': 'Precio cierre',
                                          'high': 'Precio max.', 'low': 'Precio min.', 'volume': 'Volumen'})
        if not self.df.empty:
            self.df['Fecha'] = pd.to_datetime(self.df['Fecha'])
        return self.df

    def plot_price_evolution(self):
        '''Grafica precio vs tiempo'''

        plt.figure(figsize=(10, 6))
        plt.plot(self.df['Fecha'], self.df['Precio cierre'],
                 label="Precio de Cierre", color="blue")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre (USD)")
        plt.title(f"Evolución del Precio - {self.ticker_selecc}")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

    def plot_price_and_volume(self):
        '''Grafica precio junto con el volumen cotizado'''
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(self.df['Fecha'], self.df['Precio cierre'],
                 label="Precio de Cierre", color="blue")
        ax1.set_xlabel("Fecha")
        ax1.set_ylabel("Precio de Cierre (USD)", color="blue")
        plt.grid(True)

        ax2 = ax1.twinx()
        ax2.bar(self.df['Fecha'], self.df['Volumen'],
                label="Volumen", color="gray", alpha=0.3)
        ax2.set_ylabel("Volumen", color="gray")

        plt.title(f"Evolución con Volumen - {self.ticker_selecc}")
        st.pyplot(fig)

    def plot_price_comparison(self):
        '''Grafica precio de apertura y cierre vs tiempo'''
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['Fecha'], self.df['Precio apertura'],
                 label="Precio de Apertura", color="green")
        plt.plot(self.df['Fecha'], self.df['Precio cierre'],
                 label="Precio de Cierre", color="blue")
        plt.xlabel("Fecha")
        plt.ylabel("Precio (USD)")
        plt.title(f"Comparativa de Precios - {self.ticker_selecc}")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

    def plot_candlestick(self):
        '''Confecciona el grafico de velas'''

        df_candlestick = self.df[['Fecha', 'Precio apertura',
                                  'Precio max.', 'Precio min.', 'Precio cierre']].copy()
        df_candlestick['Fecha'] = df_candlestick['Fecha'].map(mdates.date2num)

        fig, ax = plt.subplots(figsize=(10, 6))
        candlestick_ohlc(ax, df_candlestick.values, width=0.6,
                         colorup="green", colordown="red")
        ax.xaxis_date()
        ax.set_title(f"Gráfico de Velas - {self.ticker_selecc}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio (USD)")
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    def display(self):
        '''Renderiza los elementos de Streamlit'''

        st.title("Visualización de datos")

        # Columns for user inputs
        col1, col2 = st.columns(2)

        with col1:
            opciones = self.load_tickers()
            ticker_selecc = st.selectbox(
                "Seleccione un ticker para graficar", opciones, index=0)
            self.ticker_selecc = ticker_selecc.split(" - ")[0]

        with col2:
            self.tipo_grafico = st.radio("Seleccione el tipo de gráfico", [
                "Evolución del precio",
                "Evolución con volumen",
                "Comparativa entre precios (Apertura vs Cierre)",
                "Gráfico de Velas"
            ])

        if st.button("Graficar"):
            if not self.fetch_data(self.ticker_selecc).empty:
                if self.tipo_grafico == "Evolución del precio":
                    self.plot_price_evolution()
                elif self.tipo_grafico == "Evolución con volumen":
                    self.plot_price_and_volume()
                elif self.tipo_grafico == "Comparativa entre precios (Apertura vs Cierre)":
                    self.plot_price_comparison()
                elif self.tipo_grafico == "Gráfico de Velas":
                    self.plot_candlestick()

            else:
                st.warning(
                    f"No hay datos almacenados para el ticker '{self.ticker_selecc}'.")


# Crea una instancia del Visualizador y llama al metodo correspondiente
db_path = 'sqlite:////Users/requeto/Desktop/appPythonITBA/proyectoPythonITBA/finanzas_P.db'
visualizer = StockDataVisualizer(db_path)
visualizer.display()
