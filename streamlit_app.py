import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from io import StringIO
import re
import numpy as np

st.title("Álbumes de estudio de Coldplay")

# URL de la discografía de Coldplay en Wikipedia
url = "https://en.wikipedia.org/wiki/Coldplay_discography"

def extract_chart_positions(chart_str):
    """Función para extraer las posiciones de los charts de diferentes países"""
    if pd.isna(chart_str):
        return []
    
    # Expresión regular para encontrar pares de 'País: Posición' en el texto
    pattern = r'([A-Za-z\s]+):\s*(\d+)'
    matches = re.findall(pattern, chart_str)
    
    # Devolver las posiciones numéricas de cada país
    return [int(position) for country, position in matches]

try:
    # Descargar y parsear la página
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar todas las tablas tipo "wikitable"
    tables = soup.find_all("table", {"class": "wikitable"})

    # Usar la primera tabla (álbumes de estudio)
    html_str = str(tables[0])
    studio_albums = pd.read_html(StringIO(html_str))[0]

    # Seleccionar y renombrar columnas relevantes
    studio_albums = studio_albums[['Title', 'Details', 'Peak chart positions']]
    studio_albums = studio_albums.rename(columns={
        'Title': 'Título',
        'Details': 'Detalles',
        'Peak chart positions': 'Posición en rankings'
    })

    # Mostrar la tabla
    st.subheader("Tabla de álbumes de estudio")
    st.dataframe(studio_albums)

    # Asegurarnos de que la columna 'Detalles' esté en formato texto
    studio_albums['Detalles'] = studio_albums['Detalles'].astype(str)

    # Extraer el año desde la columna "Detalles"
    studio_albums['Año'] = studio_albums['Detalles'].str.extract(r'(\d{4})').astype(float)
    studio_albums['Década'] = (studio_albums['Año'] // 10 * 10).astype(int)

    st.write("Estructura del DataFrame:")
    st.write(studio_albums)

except Exception as e:
    st.error(f"Ocurrió un error al obtener los datos: {e}")
