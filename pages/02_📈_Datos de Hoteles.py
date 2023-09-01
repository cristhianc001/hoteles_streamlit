import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from data import df
import re
import demoji
import nltk
from nltk import word_tokenize

stopwords_nltk = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
       "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
       'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
       'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
       'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
       'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
       'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
       'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
       'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
       'by', 'for', 'with', 'about', 'against', 'between', 'into',
       'through', 'during', 'before', 'after', 'above', 'below', 'to',
       'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
       'again', 'further', 'then', 'once', 'here', 'there', 'when',
       'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
       'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
       'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
       'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
       'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
       "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
       'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
       'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
       'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
       'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'hotel',
       'positive', 'negative']

def remove_stopwords(text):
  tokens = word_tokenize(text) # TOKENIZA EL TEXTO EN PALABRAS SINGULARES
  filtered_sentence = [] # CREA UNA LISTA VACIA
  for i in tokens:
    if i not in stopwords_nltk: # SI LA PALABRA NO ESTA EN LA LISTA DE STOPWORDS, LA GUARDA EN LA LISTA VACIA
        filtered_sentence.append(i)

  return " ".join(filtered_sentence) # JUNTA LAS PALABRAS DE LA LISTA

def cleaning_text(text):
# TRATAR TRADUCCIONES EN REVIEWS, BORRA EL STRING "(ORIGINAL)" Y TODO A SU DERECHA
  keyword = "(Original)"
  keyword_index = text.find(keyword) # Encontrar la posición de la palabra clave
  if keyword_index != -1:
      text = text[:keyword_index + len(keyword)] # Eliminar todo después de la palabra clave

  text = text.replace("(Original)", "")
  text = text.replace("(Translated by Google)", "")

# TRATAR EMOJIS
  text = demoji.replace_with_desc(text, ' ') # reemplaza los emojis con palabras mas un espacio entre si

# BORRAR SALTOS DE LINEA
  text = text.replace("\n", " ")
# BORRAR CARACTERES NO ALFANUMERICOS
  text = re.sub(r'[^\w\s]', '', text)
# BORRAR ESPACIOS AL PRINCIPIO Y AL FINAL Y CONVERTIR A MINUSCULAS
  text = text.strip()
  text = text.lower()
# DESPUES DE LIMPIADO VERIFICAR SI HAY CARACTERES O NO, SI NO HAY CONVERTIRLOS EN NULO
  if not text:
      return None
  return text

# Lista de opciones para la lista desplegable
opciones = ["Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive", "Ramada by Wyndham New York Times Square West",
            "Ramada Plaza by Wyndham West Hollywood Hotel & Suites",  "Ramada by Wyndham Reno Hotel & Casino", 
            "Ramada by Wyndham Houston Intercontinental Airport South", "Ramada by Wyndham Houston Intercontinental Airport East"]

# Crear una lista desplegable en la aplicación
opcion_seleccionada = st.selectbox("Selecciona una opción:", opciones)

df_filtrado = df[df['lodging_name'] == opcion_seleccionada]

df_filtrado['cleaned'] = [cleaning_text(x) for x in df_filtrado['review'] ]
df_filtrado['transformed'] = [remove_stopwords(x) for x in df_filtrado['cleaned'] ]
text = ' '.join(df_filtrado['transformed'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Mostrar la WordCloud
st.image(wordcloud.to_array())

# Mostrar las opiniones correspondientes al hotel seleccionado
st.write("Opiniones para", opcion_seleccionada)
st.write(df_filtrado['cleaned'].tolist())

