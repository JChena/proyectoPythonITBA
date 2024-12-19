# Trabajo práctico final - Python - ITBA 2024

## Data Shares: Captura, Actualización y Visualización de Datos Financieros con Streamlit.

Data Shares es una aplicación desarrollada en Python que facilita la gestión y análisis de datos financieros provenientes de una API externa.

## Tabla de contenidos

1. Descripción del proyecto
2. Estructura del proyecto
3. Instalación y ejecución del proyecto
4. Uso de la aplicación
5. Base de datos
6. Tecnologías utilizadas
7. Autores

---

### 1. Descripción del proyecto

Este proyecto es una aplicación web interactiva desarrollada con _Python_ y _Streamlit_, diseñada para la gestión, visualización y análisis de datos financieros. La aplicación permite actualizar datos desde la API de Polygon.io, visualizarlos en formato tabular y generar gráficos para analizar tendencias y comportamientos de precios y volúmenes.

#### Características

- ⁠*Actualización de Datos:* Actualiza datos financieros desde la API de Polygon.io.

- ⁠*Visualización Tabular:* Guarda estos datos en un archivo de base de datos y permite la consulta de los mismos a través de un resumen.

- ⁠*Análisis Gráfico:* Permite generar gráficos de evolución de precios, volumen y gráficos de velas.

---

### 2. Estructura del Proyecto

```⁠
Proyecto/
│
├── main.py # Archivo principal para ejecutar la aplicación
├── finanzas_P.db # Base de datos SQLite3
│
├── pages/ # Subcarpeta de páginas
│ ├── ppal.py # Página para actualizar datos
│ ├── datos_BD.py # Página para visualizar datos tabulares
│ ├── graficas.py # Página para generar gráficos
├── company_tickers.json # Archivo con los codigos tickers existentes
│
└── static/ # Archivos estáticos
  └── logo3.png # Logo de la aplicación
```

---

### 3. Instalación y ejecución del proyecto

#### I.⁠ ⁠Clonar el repositorio:

```py
git clone https://github.com/JChena/proyectoPythonITBA.git
```

#### II.⁠ Crear un entorno virtual de trabajo para administrar las dependencias.

> Recomendamos utilizar _Mini_ Conda para la instalación de Python, y _pip_ para la instalación del resto de los módulos.

> ⁠Instalar las dependencias necesarias:

```py
conda create -n <env>
conda activate <env>
conda install python==3.10.13
pip install -r requirements.txt
```

⁠Las siguientes bibliotecas deben estar instaladas:

- streamlit ⁠
- pandas ⁠
- ⁠sqlalchemy ⁠
- ⁠matplotlib ⁠
- ⁠mplfinance ⁠
- ⁠requests ⁠
- json
- datetime

> ⁠Asegurarse de que el archivo finanzas_P.db esté presente en la raíz del proyecto.

#### III. Una vez instaladas las dependencias, la aplicación se lanza en un navegador mediante el siguiente comando:

```py
streamlit run src/main.py
```

⁠-----

### 4. Uso de la aplicación.

#### Requisitos de uso: generación de Clave para Uso de la API

- **Clave API**: Para usar la API de Polygon, necesitarás una API Key personalizada.
  Sigue estos pasos para obtener la tuya:

  1.1. **Regístrate en Polygon.io**: Ve a [Polygon.io](https://polygon.io/) y crea una cuenta.

  1.2. **Genera tu API Key**: Una vez que hayas iniciado sesión, dirígete a la sección de API Keys en tu cuenta y genera una nueva clave.

  1.3. **Actualiza el código**: Sustituye la línea `API_KEY = "TU_API_KEY_AQUI"` en el archivo ppal.py reemplazando el valor de la variable api_key.

#### Opciones de Uso

1.⁠ ⁠*Navegar por las diferentes páginas:*

    - _Actualizar Datos:_ Permite seleccionar un ticker y un rango de fechas para obtener datos actualizados.
    - _Mostrar Resumen:_ Muestra los datos almacenados en formato tabular interactivo.
    - _Graficar Ticker:_ Permite generar gráficos interactivos para analizar los datos financieros.

2.⁠ ⁠*Actualizar Datos:*

    - Selecciona un ticker de la lista.
    - Indica un rango de fechas.
    - Presiona el botón "Actualizar".

3.⁠ ⁠*Graficar Ticker:*

    - Selecciona un ticker y el tipo de gráfico.
    - Presiona el botón "Graficar".
    - Puedes optar por visualizar la tabla de datos que genero el gráfico.

---

### 5. Base de Datos

El gestor de base de datos utilizado es **SQLite**, que interactúa con el archivo `finanzas_P.db` donde se almacenan los datos financieros obtenidos desde la API.

#### Tablas

#### **financial_data_polygon**: almacena los datos financieros históricos de los tickers seleccionados por el usuario.

| Columna        | Tipo de Dato | Descripción                                                                             | Clave |
| -------------- | ------------ | --------------------------------------------------------------------------------------- | ----- |
| `id`           | `INTEGER`    | Identificador autoincremental único de cada registro. Es la clave primaria de la tabla. | PK    |
| `ticker`       | `TEXT`       | Símbolo bursátil del activo (Ej. AAPL, TSLA). Referencia a la tabla `maestra_tickers`.  | FK    |
| `date`         | `DATE`       | Fecha del registro, formato `YYYY-MM-DD`.                                               |       |
| `volume`       | `REAL`       | Volumen de transacciones del activo en el día especificado.                             |       |
| `vwap`         | `REAL`       | Promedio ponderado por volumen (VWAP) del día.                                          |       |
| `open`         | `REAL`       | Precio de apertura del activo en el día especificado.                                   |       |
| `close`        | `REAL`       | Precio de cierre del activo en el día especificado.                                     |       |
| `high`         | `REAL`       | Precio máximo alcanzado por el activo en el día especificado.                           |       |
| `low`          | `REAL`       | Precio mínimo alcanzado por el activo en el día especificado.                           |       |
| `transactions` | `INTEGER`    | Número de transacciones realizadas en el día.                                           |       |

#### **maestra_tickers**: tabla de referencia para validar los tickers.

| Columna           | Tipo de Dato | Descripción                                             | Clave |
| ----------------- | ------------ | ------------------------------------------------------- | ----- |
| `ticker`          | `TEXT`       | Símbolo bursátil único de la compañía (Ej. AAPL, TSLA). | PK    |
| `nombre_compania` | `TEXT`       | Nombre completo de la compañía asociada al ticker.      |       |

---

### 6. Tecnologías Utilizadas

•⁠ ⁠*Lenguaje:* Python 3.10.13

•⁠ ⁠*Librerías:*

- *⁠Streamlit* ⁠ para la interfaz web.
- *⁠Pandas* para el manejo de datos.
- _SQLite 3_ para gestionar la base de datos.
- _⁠SQLAlchemy_ para la interacción con la base de datos.
- *⁠Matplotlib* ⁠y *mplfinance* ⁠ para la generación de gráficos.
- *⁠Requests* ⁠para realizar solicitudes a la API.

---

### 7. Autores

- [Julieta Chena Mathov](https://github.com/JChena/)
- [Tamara Lourdes Parapugna](https://github.com/tamaralourdes)
- [Fabián Alberto Ghi](https://github.com/fabianghi)
- [Alejandro Terreros](https://github.com/ale8105)
