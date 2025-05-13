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
    if pd.isna(chart_str):  # Verificar si el valor es NaN
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

    # Extraer posiciones de los charts
    studio_albums['Posiciones'] = studio_albums['Posición en rankings'].apply(extract_chart_positions)

    # Crear un DataFrame para las posiciones
    chart_positions = studio_albums.explode('Posiciones')
    chart_positions['Posiciones'] = chart_positions['Posiciones'].astype(int)

    # Agrupar por título y sumar las posiciones
    chart_positions_grouped = chart_positions.groupby('Título')['Posiciones'].sum().reset_index()

    # Crear gráfico de barras
    st.subheader("Gráfico de posiciones en los charts")
    fig, ax = plt.subplots()
    ax.barh(chart_positions_grouped['Título'], chart_positions_grouped['Posiciones'], color='skyblue')
    ax.set_xlabel('Posición en rankings')
    ax.set_title('Posiciones en rankings de álbumes de estudio de Coldplay')
    st.pyplot(fig)

    # Mostrar un gráfico de líneas de las posiciones en los charts
    st.subheader("Gráfico de líneas de posiciones en los charts")
    fig, ax = plt.subplots()
    ax.plot(chart_positions_grouped['Título'], chart_positions_grouped['Posiciones'], marker='o', color='orange')
    ax.set_xlabel('Álbumes')
    ax.set_ylabel('Posición en rankings')
    ax.set_title('Posiciones en rankings de álbumes de estudio de Coldplay')
    ax.set_xticklabels(chart_positions_grouped['Título'], rotation=45, ha='right')
    st.pyplot(fig)

except Exception as e:
    st.error(f"Ocurrió un error al obtener los datos: {e}")
