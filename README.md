# Data Shares (version_consola)

Esta versión del proyecto es un sistema desarrollado en Python que facilita la gestión y análisis de datos financieros provenientes de una API externa.

---

## Tabla de Contenidos
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Integrantes](#integrantes)
3. [Estructura del Repositorio](#estructura-del-repositorio)
4. [Instalación y Configuración del Proyecto](#instalación-y-configuración-del-proyecto)
5. [Código del Menú](código-del-menú)
6. [Detalle del Query Map](#detalle-del-query-map)
7. [Base de Datos](#base-de-datos)

---

## Descripción del Proyecto

El proyecto permite a los usuarios:
- Consultar datos financieros de los tickers vigentes en el mercado.
- Guardar estos datos en un archivo de base de datos. 
- Generar y visualizar gráficos financieros, incluyendo gráficos de velas, evolución de precios y análisis de volumen.
- Consultar datos almacenados a través de un resumen.

---

## Integrantes

- Julieta Chena Mathov
- Tamara Lourdes Parapugna 
- Fabián Alberto Ghi
- Alejandro Terreros

---
## Estructura del Repositorio
El repositorio está alojado en GitHub y consta de dos ramas (version_consola y version_streamlit). Ambas contienen el mismo proyecto, pero la principal diferencia es que version_streamlit usa Streamlit para visualizar la aplicación en un navegador web. 

### Contenido version_consola
- Una carpeta **`scripts`**, que incluye los siguientes archivos:
  - `crear_BD.py`
  - `version_consola.py`
- Un archivo `company_tickers.json` (necasario para correr datos_BD)
- Un archivo `README.md` que contiene la descripción del proyecto en version_consola.
- Un archivo `requirements.txt` que detalla las dependencias necesarias para ejecutar el proyecto.
---

## Instalación y Configuración del Proyecto

### 1. Generación de Clave para Uso de la API
- **Clave API**: Para usar la API de Polygon, necesitarás una API Key personalizada.
   > A fin de probar la aplicación, ésta tiene al momento, una API Key incorporada en el código que será reemplazada, luego de la correción del proyecto, por una variable en la que futuros usuarios puedan almacenar su API Key personal.
- Sigue estos pasos para obtener la tuya:
  
  1.1. **Regístrate en Polygon.io**: Ve a [Polygon.io](https://polygon.io/) y crea una cuenta.
  
  1.2. **Genera tu API Key**: Una vez que hayas iniciado sesión, dirígete a la sección de API Keys en tu cuenta y genera una nueva clave.
  
  1.3. **Actualiza el código**: Sustituye la línea `API_KEY = "TU_API_KEY_AQUI"` en el archivo `version_consola.py` del proyecto.  

### 2. Instalación de Miniconda y Visual Studio Code
- Descarga e instala **Miniconda** desde [su sitio oficial](https://docs.conda.io/en/latest/miniconda.html).  
- Descarga e instala **Visual Studio Code** desde [su sitio oficial](https://code.visualstudio.com/).

### 3. Configuración del Entorno de Trabajo
3.1. **Abrir terminal Miniconda** y ubicarse en la carpeta de trabajo.
3.2. **Clonar el repositorio** :
```bash
git clone https://github.com/JChena/proyectoPythonITBA.git
```
3.3. **Ubicarse en la carpeta proyectoPythonITBA**
3.4. **Ubicarse en la rama version_consola** 
```bash
git checkout version_consola
```  
3.5. **Genera un entorno de trabajo** desde Miniconda ejecutando el siguiente comando en la terminal:  
```bash
conda create --name <nombre_del_entorno> 
```
```bash
conda activate <nombre_del_entorno> 
```
3.6. **Instala Python 3.10.13** 
```bash
conda install python==3.10.13
```
3.7. **Instala las dependencias usando pip** (todas se encuentran en el archivo requirements.txt):
```bash
pip install -r requirements.txt
```

### 4. Configuración de Visual Studio Code
- Abre Visual Studio Code desde la terminal de Miniconda con:
```bash
code .
```
Asegúrate de que el entorno creado en el paso 3 esté activo en Visual Studio Code. Para verificar, selecciona el intérprete de Python correcto en la esquina inferior izquierda.

### 5. Orden de Ejecución de los Scripts

5.1. Corre el script `crear_BD`. Esto creará una base de datos llamada `finanzas.db` en tu carpeta de trabajo.

5.2. Corre el script `version_consola.py`. Esto navegará por el proyecto.

---

## Código

El script está escrito utilizando la programación orientada a objetos. Las clases son:

1. **Validador**: Contiene métodos estáticos para validar fechas y tickers.
2. **BaseDeDatos**: Maneja la conexión, almacenamiento y consultas a la base de datos mediante el gestor SQLite.
3. **APIManager**: Gestiona las solicitudes de datos a la API de Polygon.
4. **Graficador**: Proporciona métodos para generar gráficos financieros.
5. **Menu**: Presenta un menú interactivo para el usuario y conecta todas las funcionalidades.

### Opciones del Menú Principal
1. **Actualizar Datos**: Permite ingresar un ticker, un rango de fechas, y actualizar la base de datos con datos requeridos a la API.
2. **Visualizar Datos**: Redirige a un submenú que proporciona opciones para generar gráficos o consultar resúmenes de los datos almacenados.
3. **Salir**: Cierra el programa y la conexión a la base de datos.

### Submenú Visualizar Datos
1. **Resumen de Datos Almacenados**: Muestra un resumen de los datos disponibles en la base de datos, filtrado por ticker o rango de fechas.  
2. **Gráficos**: Redirige a un submenú que proporciona diferentes opciones de generación de gráficos financieros. 
3. **Volver al menú principal**.   

### Submenú Gráficos
1. **Evolución del Precio de Cierre**: Muestra la evolución histórica del precio de cierre para un ticker.
2. **Evolución con Volumen**: Combina la evolución del precio de cierre con un análisis del volumen de transacciones.
3. **Comparativa entre Precios (Apertura vs Cierre)**: Compara precios de apertura y cierre en un gráfico.
4. **Gráfico de Velas**: Genera un gráfico de velas tradicional.
5. **Volver al submenú de Visualizar Datos**.

### Notas Adicionales sobre el Menú

- Cada opción del menú está conectada a funciones específicas dentro del programa.  
- El submenú de **Visualizar Datos** está diseñado para que sea fácil alternar entre resúmenes tabulares y gráficos visuales.  

---
## Detalle del Query Map

El `query_map` es una estructura utilizada para mapear opciones del menú a consultas SQL específicas que extraen datos de la base de datos. Su propósito es simplificar el manejo de las consultas según el gráfico solicitado.

### Estructura del Query Map

```python
query_map = {
    "1": "SELECT date, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
    "2": "SELECT date, close, volume FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
    "3": "SELECT date, open, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
    "4": "SELECT date, open, high, low, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC",
}
```

### Ejemplo de Uso
Cuando el usuario selecciona una opción del submenú de gráficas, el programa utiliza el `query_map` para determinar qué consulta ejecutar. Por ejemplo:

- Si el usuario selecciona **1. Evolución del Precio de Cierre**, se ejecuta la consulta:
  ```sql
  SELECT date, close FROM financial_data_polygon WHERE ticker = ? ORDER BY date ASC
  ```
  Esto devuelve las fechas y precios de cierre ordenados para el ticker especificado.

- El resultado de esta consulta se pasa al método correspondiente de la clase `Graficador` para generar el gráfico deseado.

Esto permite separar claramente la lógica (consultas SQL) de la visualización (métodos de graficación).

---
## Base de Datos

El gestor de base de datos utilizado es **SQLite**, que interactúa con un archivo llamado `finanzas.db`. Este archivo actúa como la base de datos donde se almacenan los datos financieros obtenidos desde la API. 

### Tablas 

- **financial_data_polygon**: Almacena los datos financieros históricos de los tickers.
  - Columnas principales: `ticker`, `date`, `volume`, `vwap`, `open`, `close`, `high`, `low`, `transactions`.

| Columna       | Tipo de Dato | Descripción                                                                 | Clave   |
|---------------|--------------|-----------------------------------------------------------------------------|---------|
| `id`          | `INTEGER`    | Identificador autoincremental único de cada registro. Es la clave primaria de la tabla.      | PK      |
| `ticker`      | `TEXT`       | Símbolo bursátil del activo (Ej. AAPL, TSLA). Referencia a la tabla `maestra_tickers`. |         |
| `date`        | `DATE`       | Fecha del registro, formato `YYYY-MM-DD`.                                   |         |
| `volume`      | `REAL`       | Volumen de transacciones del activo en el día especificado.                 |         |
| `vwap`        | `REAL`       | Promedio ponderado por volumen (VWAP) del día.                              |         |
| `open`        | `REAL`       | Precio de apertura del activo en el día especificado.                       |         |
| `close`       | `REAL`       | Precio de cierre del activo en el día especificado.                         |         |
| `high`        | `REAL`       | Precio máximo alcanzado por el activo en el día especificado.               |         |
| `low`         | `REAL`       | Precio mínimo alcanzado por el activo en el día especificado.               |         |
| `transactions`| `INTEGER`    | Número de transacciones realizadas en el día.                               |         |

- **maestra_tickers**: Una tabla de referencia para validar los tickers.

| Columna         | Tipo de Dato | Descripción                                                        | Clave   |
|-----------------|--------------|--------------------------------------------------------------------|---------|
| `ticker`        | `TEXT`       | Símbolo bursátil único de la compañía (Ej. AAPL, TSLA).            | PK      |
| `nombre_compania`| `TEXT`      | Nombre completo de la compañía asociada al ticker.                 |         |

---

¡Gracias por usar este programa! 

