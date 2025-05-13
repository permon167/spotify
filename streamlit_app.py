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

    # Extraer posiciones de charts
    studio_albums['Posición en rankings'] = studio_albums['Posición en rankings'].apply(extract_chart_positions)
    # Hacer un grafico con las posiciones de los charts
    # Crear un gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    for index, row in studio_albums.iterrows():
        positions = row['Posición en rankings']
        if not pd.isna(positions) and len(positions) > 0:  # Verificar si hay posiciones disponibles
            ax.bar(row['Título'], positions[0], label=row['Título'])
    # Configurar el gráfico
    ax.set_xlabel('Álbumes')
    ax.set_ylabel('Posición en rankings')
    ax.set_title('Posiciones de álbumes de estudio de Coldplay en rankings')
    ax.legend()
    # Mostrar el gráfico
    st.subheader("Gráfico de posiciones en rankings")
    st.pyplot(fig)

except Exception as e:
    st.error(f"Ocurrió un error al obtener los datos: {e}")
