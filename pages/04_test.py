########### LIBRERIAS

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
import random

########### TITULO
st.title('Revision de reseñas')
st.markdown('***')

########### VARIABLES Y FUNCIONES
# Lista de opciones para la lista desplegable
opciones = ["Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive", "Ramada by Wyndham New York Times Square West",
            "Ramada Plaza by Wyndham West Hollywood Hotel & Suites",  "Ramada by Wyndham Reno Hotel & Casino", 
            "Ramada by Wyndham Houston Intercontinental Airport East"]

@st.cache_data
def load_data():
    df = pd.read_parquet("data/reviews-model.parquet")
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
elif opcion_hotel == "Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive":
    hotel = 1076
elif opcion_hotel == "Ramada Plaza by Wyndham West Hollywood Hotel & Suites":
    hotel = 1159
elif opcion_hotel == "Ramada by Wyndham New York Times Square West":
    hotel = 1725
elif opcion_hotel == "Ramada by Wyndham Houston Intercontinental Airport East":
    hotel = 1520

if sentimiento is None:
    df_filtrado = df[(df['lodging_id'] == hotel)]
else:
    df_filtrado = df[(df['lodging_id'] == hotel) & (df[categoria] == sentimiento)]

# Mostrar la WordCloud
st.image(WC(df_filtrado).to_array())

# Mostrar las opiniones correspondientes al hotel seleccionado
reviews_filtradas = df_filtrado[df_filtrado[categoria] != 0]
st.write("Opiniones para", opcion_hotel)
st.write(reviews_filtradas['review'].tolist())