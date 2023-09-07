########### LIBRERIAS

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from datetime import datetime

########### TITULO
st.title('Revision de reseñas')
st.markdown('***')

########### VARIABLES Y FUNCIONES
# Lista de opciones para la lista desplegable
opciones = ["Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive", "Ramada by Wyndham New York Times Square West",
            "Ramada Plaza by Wyndham West Hollywood Hotel & Suites",  "Ramada by Wyndham Reno Hotel & Casino", 
            "Ramada by Wyndham Houston Intercontinental Airport East"]

# Hotels de competencia
lista_id_NV = [855,851]
lista_id_FL = [1010,1062]
lista_id_CA = [1164,1175,1653]
lista_id_NY = [1328,1366,1356]
lista_id_TX = [1521,1517]

@st.cache_data
def load_data():
    df = pd.read_parquet("data/reviews-model.parquet")
    df["date"] = [datetime.strptime(x, "%Y-%m-%d").date() for x in df["date"]]
    return df
df = load_data()

@st.cache_resource
def download_punkt():
    nltk.download('punkt')

download_punkt()

def WC(df_wc):
    # tokenizando
    text = df_wc['clean_stopwords'].str.cat()
    text = text.lower()  # Convierte a minúsculas
    text = ''.join([c for c in text if c.isalpha() or c.isspace()])
    words = nltk.word_tokenize(text)

    # Análisis de frecuencia de palabras
    freq_dist = nltk.FreqDist(words)
    # Creación de la Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dist)
    
    return wordcloud  # Devuelve directamente el objeto WordCloud

########### CONTENIDO
# Agregar filtros de fecha
st.sidebar.header("Filtros de Fecha")
fecha_minima = pd.to_datetime(min(df["date"]))
fecha_maxima = pd.to_datetime(max(df["date"]))

fecha_inicio = st.sidebar.date_input("Fecha de Inicio", min_value = fecha_minima, max_value = fecha_maxima, value=fecha_minima)
fecha_fin = st.sidebar.date_input("Fecha de Fin", min_value = fecha_minima, max_value = fecha_maxima, value=fecha_maxima)

opcion_sentimiento = st.sidebar.radio("Seleccione una opcion de sentimiento:", ["Positivo", "Negativo", "Total"])
if opcion_sentimiento == "Positivo":
    sentimiento = 1
elif opcion_sentimiento == "Negativo":
    sentimiento = -1
elif opcion_sentimiento == "Total":
    sentimiento = None

opcion_categoria = st.sidebar.radio("Seleccione una categoria:", ["Habitación", "Atención al cliente", "Limpieza", "Desayuno"])
if opcion_categoria == "Habitación":
    categoria = "room_sentiment"
elif opcion_categoria == "Atención al cliente":
    categoria = "guest_service_sentiment"
elif opcion_categoria == "Limpieza":
    categoria = "cleaning_sentiment"
elif opcion_categoria == "Desayuno":
    categoria = "breakfast_sentiment"


# Crear una lista desplegable en la aplicación
opcion_hotel = st.selectbox("Selecciona un hotel:", opciones)
if opcion_hotel == "Ramada by Wyndham Reno Hotel & Casino":
    hotel = 811
    lista_comp = lista_id_NV
elif opcion_hotel == "Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive":
    hotel = 1076
    lista_comp = lista_id_FL
elif opcion_hotel == "Ramada Plaza by Wyndham West Hollywood Hotel & Suites":
    hotel = 1159
    lista_comp = lista_id_CA
elif opcion_hotel == "Ramada by Wyndham New York Times Square West":
    hotel = 1725
    lista_comp = lista_id_NY
elif opcion_hotel == "Ramada by Wyndham Houston Intercontinental Airport East":
    hotel = 1520
    lista_comp = lista_id_TX

# Hoteles de Ramada
if sentimiento is None:
    df_filtrado = df[(df['lodging_id'] == hotel) & (df['date'] >= fecha_inicio) & (df['date'] <= fecha_fin)]
else:
    df_filtrado = df[(df['lodging_id'] == hotel) & (df[categoria] == sentimiento)  & (df['date'] >= fecha_inicio) & (df['date'] <= fecha_fin)]
# Hoteles de la competencia
if sentimiento is None:
    df_filtrado_comp = df[df['lodging_id'].isin(lista_comp)  & (df['date'] >= fecha_inicio) & (df['date'] <= fecha_fin)]
else:
    df_filtrado_comp = df[(df['lodging_id'].isin(lista_comp)) & (df[categoria] == sentimiento)  & (df['date'] >= fecha_inicio) & (df['date'] <= fecha_fin)]

# Mostrar la WordCloud
st.markdown(f"Nube de palabras para la categoría: **{opcion_categoria}** con sentimientos: **{opcion_sentimiento}** para el hotel: ***{opcion_hotel}***")
st.image(WC(df_filtrado).to_array())

st.markdown(f"Nube de palabras para la categoría: **{opcion_categoria}** con sentimientos: **{opcion_sentimiento}** para la ***competencia***")
st.image(WC(df_filtrado_comp).to_array())

# Mostrar las opiniones correspondientes al hotel seleccionado
st.markdown(f"Opiniones para: ***{opcion_hotel}***")
st.write(df_filtrado['review'].tolist())