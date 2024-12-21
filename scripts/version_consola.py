import datetime
import requests
import sqlite3
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import matplotlib.dates as mdates
import mplfinance as mpf
import pandas as pd

class Validador:
    """Clase para validar datos de entrada"""

    @staticmethod
    def validar_fecha(fecha_str):
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Fecha inválida. Por favor, use el formato YYYY-MM-DD.")
            return None

    @staticmethod
    def validar_ticker(ticker):
        try:
            # Verificar si el ticker puede convertirse en un número
            float(ticker)
            print("Ticker inválido. No puede ser un número.")
            return None
        except ValueError:
            # Si no es un número, validar que sea un string no vacío
            if isinstance(ticker, str) and ticker.strip():
                # Validar si el ticker existe en la tabla maestra
                conexion = sqlite3.connect("finanzas.db")
                cursor = conexion.cursor()

                consulta = "SELECT COUNT(*) FROM maestra_tickers WHERE ticker = ?"
                cursor.execute(consulta, (ticker,))
                resultado = cursor.fetchone()[0]  # Devuelve el número de registros encontrados
                conexion.close()

                if resultado == 0:
                    print(f"Error: El ticker '{ticker}' no es un código de ticker válido.")
                    return None
                else:
                    return ticker.strip()

            else:
                print("Ticker inválido. Debe ser un texto no vacío.")
                return None


class BaseDeDatos:
    """Clase para manejar la conexión y consultas a la base de datos"""
    def __init__(self):
        self.conexion = sqlite3.connect("finanzas.db")
        self.cursor = self.conexion.cursor()

    def cerrar_conexion(self):
        self.conexion.close()

    def guardar_datos(self, ticker, resultados):
      if not resultados:  # Verificar si resultados es None o vacío
          print("No hay resultados para guardar en la base de datos.")
          return  # Salir de la función si no hay datos

      for dato in resultados:
          date = datetime.datetime.utcfromtimestamp(dato['t'] / 1000).strftime('%Y-%m-%d')
          volume = dato['v']
          vwap = dato['vw']
          open_price = dato['o']
          close_price = dato['c']
          high = dato['h']
          low = dato['l']
          transactions = dato['n']

          self.cursor.execute('''
              INSERT INTO financial_data_polygon (ticker, date, volume, vwap, open, close, high, low, transactions)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
          ''', (ticker, date, volume, vwap, open_price, close_price, high, low, transactions))

      self.conexion.commit()
      print("Datos guardados en la base de datos correctamente.")


    def consultar_datos(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


class APIManager:
    """Clase para manejar solicitudes a la API"""
    API_KEY = "7EuDFFydcjhpG3G0JaoJmBUgpNDOZnp8"

    @staticmethod
    def solicitar_datos(ticker, fecha_inicio, fecha_fin):
        conexion = sqlite3.connect("finanzas.db")
        cursor = conexion.cursor()

        # Verificar los rangos existentes en la base de datos para el ticker
        consulta = """
        SELECT MIN(date), MAX(date) FROM financial_data_polygon WHERE ticker = ?
        """
        cursor.execute(consulta, (ticker,))
        resultado = cursor.fetchone()
        conexion.close()

        rango_faltante = []

        if resultado and resultado[0] and resultado[1]:
            # Rango existente en la base de datos
            fecha_guardada_inicio, fecha_guardada_fin = resultado
            fecha_guardada_inicio = datetime.datetime.strptime(fecha_guardada_inicio, "%Y-%m-%d")
            fecha_guardada_fin = datetime.datetime.strptime(fecha_guardada_fin, "%Y-%m-%d")
        
            #print(type(fecha_inicio)) #str
            #print(type(fecha_guardada_inicio)) #datetime

        # Si el rango solicitado está parcialmente fuera de los datos existentes
            if fecha_inicio < fecha_guardada_inicio:
                rango_faltante.append((fecha_inicio.strftime("%Y-%m-%d"),(fecha_guardada_inicio - datetime.timedelta(days=1)).strftime("%Y-%m-%d")))

            if fecha_fin > fecha_guardada_fin:
                rango_faltante.append(((fecha_guardada_fin + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                                      fecha_fin.strftime("%Y-%m-%d")))
        else:
            # No hay datos en la base de datos, pedir todo el rango solicitado
            rango_faltante.append((fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")))

        # Solicitar datos para los rangos faltantes
        for inicio, fin in rango_faltante:
            if inicio <= fin:  # Evitar rangos inválidos o vacíos
                print(f"Pidiendo datos para el ticker '{ticker}' desde {inicio} hasta {fin}...")
                APIManager.llamar_api_y_guardar(ticker, inicio, fin)


    @staticmethod
    def llamar_api_y_guardar(ticker, fecha_inicio, fecha_fin):
      url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio}/{fecha_fin}"
      params = {"sort": "asc", "apiKey": APIManager.API_KEY}
      response = requests.get(url, params=params)

      if response.status_code == 200:
          datos = response.json()
          if datos.get('results'):  # Verifica si hay resultados válidos
              BaseDeDatos().guardar_datos(ticker, datos['results'])
          else:
              print(f"No hay resultados para guardar en la base de datos para el rango {fecha_inicio} a {fecha_fin}.")
      else:
          print(f"Error al pedir datos. Código de estado: {response.status_code}")


class Graficador:
    """Clase para manejar las operaciones de graficación"""
    @staticmethod
    def graficar_ticker(datos, ticker):
        fechas = [fila[0] for fila in datos]
        precios_cierre = [fila[1] for fila in datos]

        plt.figure(figsize=(10, 6))
        plt.plot(fechas, precios_cierre, marker="o", linestyle="-", color="b", label=f"{ticker} - Precio de Cierre")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre (USD)")
        plt.title(f"Evolución del Precio de Cierre para {ticker}")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def graficar_velas(datos, ticker):
        columnas = ["Date", "Open", "High", "Low", "Close"]
        df = pd.DataFrame(datos, columns=columnas)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        mpf.plot(
            df,
            type='candle',
            style='charles',
            title=f"Gráfico de Velas para {ticker}",
            ylabel="Precio (USD)",
            volume=False
        )

    @staticmethod
    def graficar_con_volumen(datos, ticker):
        fechas = [fila[0] for fila in datos]
        precios_cierre = [fila[1] for fila in datos]
        volumen = [fila[2] for fila in datos]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.plot(fechas, precios_cierre, color='b', label='Precio de Cierre', marker='o')
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Precio de Cierre (USD)', color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        ax2 = ax1.twinx()
        ax2.bar(fechas, volumen, color='g', alpha=0.3, label='Volumen')
        ax2.set_ylabel('Volumen', color='g')
        ax2.tick_params(axis='y', labelcolor='g')

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.title(f'Evolución del Precio de Cierre y Volumen para {ticker}')
        plt.show()

    @staticmethod
    def graficar_comparativa(datos, ticker):
        fechas = [fila[0] for fila in datos]
        apertura = [fila[1] for fila in datos]
        cierre = [fila[2] for fila in datos]

        plt.figure(figsize=(10, 6))
        plt.plot(fechas, apertura, marker="o", linestyle="-", color="r", label="Precio de Apertura")
        plt.plot(fechas, cierre, marker="o", linestyle="-", color="b", label="Precio de Cierre")
        plt.xlabel("Fecha")
        plt.ylabel("Precio (USD)")
        plt.title(f"Comparativa entre Precios de Apertura y Cierre para {ticker}")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

class Menu:
    """Clase para manejar el menú principal del programa"""
    def __init__(self):
        self.db = BaseDeDatos()

    def mostrar_menu(self):
        print("\n--- Menú ---")
        print("1. Actualizar Datos")
        print("2. Visualizar Datos")
        print("3. Salir")

    def actualizar_datos(self):
        ticker = None
        while not ticker:
            ticker_input = input("Ingrese el ticker: ").upper()
            ticker = Validador.validar_ticker(ticker_input)

        fecha_inicio = None
        while not fecha_inicio:
            fecha_inicio_input = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_inicio = Validador.validar_fecha(fecha_inicio_input)

        fecha_fin = None
        while not fecha_fin:
            fecha_fin_input = input("Ingrese la fecha fin (YYYY-MM-DD): ")
            fecha_fin = Validador.validar_fecha(fecha_fin_input)

        if fecha_fin < fecha_inicio:
            print("La fecha fin no puede ser anterior a la fecha de inicio.")
            return

        datos = APIManager.solicitar_datos(ticker, fecha_inicio, fecha_fin)
       
    def mostrar_menu_visualizar_datos(self):
      while True:
          print("\n--- Submenú: Visualizar Datos ---")
          print("1. Resumen de Tickers disponibles")
          print("2. Ver Gráficas")
          print("3. Volver al Menú Principal")

          opcion = input("Seleccione una opción (1/2/3): ").strip()

          if opcion == "1":
              self.mostrar_resumen()
          elif opcion == "2":
              self.mostrar_menu_graficas()
          elif opcion == "3":
              print("Regresando al Menú Principal...\n")
              return  # Sale al menú principal
          else:
              print("Opción no válida. Intente de nuevo.")

    def mostrar_menu_graficas(self):
        ticker = None
        while not ticker:
            ticker_input = input("Ingrese el ticker a graficar: ").upper()
            ticker = Validador.validar_ticker(ticker_input)

        while True:
            print("\n--- Opciones de Gráficos ---")
            print("1. Evolución del Precio de Cierre")
            print("2. Evolución con Volumen")
            print("3. Comparativa entre Precios (Apertura vs Cierre)")
            print("4. Gráfico de Velas")
            print("5. Volver al submenú de Visualizar Datos")

            opcion = input("Seleccione una opción (1/2/3/4/5): ").strip()

            if opcion == "5":
                return  # Volver al submenú "Visualizar Datos"

            datos = None
            if opcion in ["1", "2", "3", "4"]:
                query_map = {
                    "1": "SELECT date, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
                    "2": "SELECT date, close, volume FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
                    "3": "SELECT date, open, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
                    "4": "SELECT date, open, high, low, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
                }

                query = query_map[opcion]
                datos = self.db.consultar_datos(query, (ticker,))

            if not datos:
                print(f"No hay datos almacenados para el ticker '{ticker}'.")
                continue

            if opcion == "1":
                Graficador.graficar_ticker(datos, ticker)
            elif opcion == "2":
                Graficador.graficar_con_volumen(datos, ticker)
            elif opcion == "3":
                Graficador.graficar_comparativa(datos, ticker)
            elif opcion == "4":
                Graficador.graficar_velas(datos, ticker)

            print("\nVolviendo al submenú de Visualizar Datos...\n")
            break  # Rompe el bucle actual y regresa al submenú de Visualizar Datos

    def mostrar_resumen(self):
        query = """
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
        resultados = self.db.consultar_datos(query)

        tabla = PrettyTable()
        tabla.field_names = ["Ticker", "Nombre de la Compañía", "Fecha Desde", "Fecha Hasta"]
        for fila in resultados:
            tabla.add_row(fila)

        print(tabla)

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.actualizar_datos()
            elif opcion == "2":
                self.mostrar_menu_visualizar_datos()
            elif opcion == "3":
                print("Saliendo...")
                self.db.cerrar_conexion()
                break
            else:
                print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar()
