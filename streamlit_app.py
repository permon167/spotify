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

# Descargar y parsear la página
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Buscar todas las tablas tipo "wikitable"
tables = soup.find_all("table", {"class": "wikitable"})

# La primera tabla suele ser la de álbumes de estudio
studio_albums = pd.read_html(str(tables[0]))[0]

# Mostramos solo las columnas relevantes
studio_albums = studio_albums[['Title', 'Details', 'Peak chart positions']]
# Keep all original columns and rename the 3 selected columns
column_mapping = {
    'Title': 'Título',
    'Album details': 'Detalles',
    'Peak chart positions': 'Posición en rankings'
}
studio_albums = studio_albums.rename(columns=column_mapping)
studio_albums

# Visualización simple
studio_albums.index = studio_albums['Título']  # Set the album titles as index
studio_albums.plot(kind='barh', figsize=(10,5), title="Álbumes de estudio - Coldplay",
                 y=['Posición en rankings'])  # Plot using a numeric column like 'Posición en rankings'
plt.xlabel("Álbum")
plt.tight_layout()
plt.show()