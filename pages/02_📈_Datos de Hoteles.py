import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from data import df

if st.checkbox("mostrar df"):
    st.dataframe(df)


# Lista de opciones para la lista desplegable
opciones = ["Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive", "Ramada by Wyndham New York Times Square West",
            "Ramada Plaza by Wyndham West Hollywood Hotel & Suites",  "Ramada by Wyndham Reno Hotel & Casino", 
            "Ramada by Wyndham Houston Intercontinental Airport South", "Ramada by Wyndham Houston Intercontinental Airport East"]

# Crear una lista desplegable en la aplicación
opcion_seleccionada = st.selectbox("Selecciona una opción:", opciones)

# Mostrar la opción seleccionada
st.write("Has seleccionado:", opcion_seleccionada)

df_filtrado = df[df['lodging_name'] == opcion_seleccionada]

text = ' '.join(df_filtrado['review'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Mostrar la WordCloud
st.image(wordcloud.to_array())

# Mostrar las opiniones correspondientes al hotel seleccionado
st.write("Opiniones para", opcion_seleccionada)
st.write(df_filtrado['review'].tolist())

