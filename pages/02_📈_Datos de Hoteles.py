import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_parquet("data/df_transformed.parquet")
    df["date"] = [x.date() for x in df["date"]]
    return df
df = load_data()

# Lista de opciones para la lista desplegable
opciones = ["Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive", "Ramada by Wyndham New York Times Square West",
            "Ramada Plaza by Wyndham West Hollywood Hotel & Suites",  "Ramada by Wyndham Reno Hotel & Casino", 
            "Ramada by Wyndham Houston Intercontinental Airport South", "Ramada by Wyndham Houston Intercontinental Airport East"]

# Crear una lista desplegable en la aplicación
opcion_seleccionada = st.selectbox("Selecciona una opción:", opciones)

# Agregar filtros de fecha
st.sidebar.header("Filtros de Fecha")
fecha_minima = pd.to_datetime(min(df["date"]))
fecha_maxima = pd.to_datetime(max(df["date"]))

fecha_inicio = st.sidebar.date_input("Fecha de Inicio", min_value = fecha_minima, max_value = fecha_maxima, value=fecha_minima)
fecha_fin = st.sidebar.date_input("Fecha de Fin", min_value = fecha_minima, max_value = fecha_maxima, value=fecha_maxima)

df_filtrado = df[(df['lodging_name'] == opcion_seleccionada) & (df['date'] >= fecha_inicio) & (df['date'] <= fecha_fin)]

text = ' '.join(df_filtrado['transformed'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Mostrar la WordCloud
st.image(wordcloud.to_array())

# Mostrar las opiniones correspondientes al hotel seleccionado
st.write("Opiniones para", opcion_seleccionada)
st.write("Fecha de Inicio:", fecha_inicio)
st.write("Fecha de Fin:", fecha_fin)
st.write(df_filtrado['cleaned'].tolist())

