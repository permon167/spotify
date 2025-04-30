# streamlit_app.py

import streamlit as st
import pandas as pd

# Título de la app
st.title("Álbumes de Estudio de Coldplay")
st.markdown("Scraping en vivo desde Wikipedia")

# URL de Wikipedia
url = "https://en.wikipedia.org/wiki/Coldplay_discography"

# Cargar tablas
tables = pd.read_html(url)

# Elegir tabla de álbumes de estudio (usualmente la primera)
df = tables[0]

# Seleccionar automáticamente las 3 primeras columnas (más relevantes)
columnas_interes = df.columns[:3]
albumes_estudio = df[columnas_interes]

# Mostrar tabla
st.subheader("Listado de Álbumes de Estudio")
st.dataframe(albumes_estudio)

# Opción para exportar como CSV
csv = albumes_estudio.to_csv(index=False).encode('utf-8')
st.download_button("Descargar como CSV", data=csv, file_name="coldplay_albums.csv", mime='text/csv')
