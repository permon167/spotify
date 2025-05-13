import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from io import StringIO
import re
import numpy as np
from wordcloud import wordcloud
import matplotlib.pyplot as plt 

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


st.title("Visualización de álbumes de estudio")

# Visualización simple
studio_albums.index = studio_albums['Título']  # Set the album titles as index

# Crear el gráfico con Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
studio_albums.plot(
    kind='barh',
    y=['Posición en rankings'],  # Asegúrate de que esta columna sea numérica
    ax=ax,
    title="Álbumes de estudio - Coldplay"
)
ax.set_xlabel("Posición en rankings")
ax.set_ylabel("Álbum")
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)


st.title("Análisis de letra de Canciones")

# Función para obtener la letra de una canción
def get_lyrics(artist, title):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()['lyrics']
    else:
        return "Letra no encontrada."

# Ejemplo con una canción famosa
song = "Yellow"
lyrics = get_lyrics("Coldplay", song)
print(lyrics[:500])  # Primeros 500 caracteres


wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title(f"WordCloud: {song}")
plt.show()
