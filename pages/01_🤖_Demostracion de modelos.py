########### LIBRERIAS
import pandas as pd
import ast
import streamlit as st
import openai
import re
import demoji
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

########### TITULO
st.title('Demostración de clasificación de reseñas')
st.markdown('***')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintaned by: Latam Data Consultores")

########### VARIABLES Y FUNCIONES
openai.api_key = st.secrets["API_KEY"]

@st.cache_resource
def load_analyzer():
  return SentimentIntensityAnalyzer()

analyzer = load_analyzer()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def cleaning_text(text):
# TRATAR TRADUCCIONES EN REVIEWS, BORRA EL STRING "(ORIGINAL)" Y EL RESTO A SU DERECHA
  keyword = "(Original)"
  keyword_index = text.find(keyword) # Encontrar la posición de la palabra clave
  if keyword_index != -1:
      text = text[:keyword_index + len(keyword)] # Eliminar todo después de la palabra clave

  text = text.replace("(Original)", "")
  text = text.replace("(Translated by Google)", "")
  text = demoji.replace_with_desc(text, ' ') # reemplaza los emojis con palabras mas un espacio entre si
  text = text.replace("\n", " ")
  text = re.sub(r'[^\w\s]', '', text)
  text = text.strip()
  text = text.lower()
# DESPUES DE LIMPIADO VERIFICAR SI HAY CARACTERES O NO, SI NO HAY CONVERTIRLOS EN NULO
  if not text:
      return None
  return text

def score_sentiment(text):
  if not text: 
    return 0
  else:   
    scores = analyzer.polarity_scores(text)
  return scores["compound"]

def sentiment(score):
  if score > 0.05: 
    return "positivo"
  elif score < -0.05:
    return "negativo"
  else:
     return "neutro"

########### CONTENIDO

st.markdown("""El funcionamiento de los modelos de clasificación y analisis de sentimiento pueden ser probados
         por medio de reseñas individuales introducidas en el cuadro de texto a continuación.""")

# Crear un cuadro de texto y obtener el texto ingresado por el usuario
input_text = st.text_input("Escribe una reseña aqui:")

# Verificar si el usuario ha ingresado texto y luego llamar a la función
if input_text:
    input_text = cleaning_text(input_text)
    score = score_sentiment(input_text)
    resultado =  get_completion(
        f""" 1. Give me the overall sentiment of the next review, the response can be pos for positive, neg for negative or neu for neutral.
            2. Give me the sentiment of the next categories of the review: room, guest service, cleaning and breakfast.
            The response must be pos for positive, neg for negative or neu neutral.
            3. The output must be in JSON format and the keys must be 'overall_sentiment', 'room_sentiment', 'guest_service_sentiment','cleaning_sentiment' and 'breakfast_sentiment'.
            \ ```{input_text}``` """)
    
    resultado = ast.literal_eval(resultado)
    df = pd.DataFrame([resultado])
    st.markdown("### Sentimiento por categoria:")
    st.dataframe(df)
    st.write("""El resultado de sentimiento por categoria se divide por 'pos' siendo positivo, 'neu' neutral y 'neg' negativo. 
            Ademas de su categorización por servicios del hotel: estado de la habitación, atención al cliente, limpieza y desayuno.
            """)

    st.markdown(f"### Puntaje de sentimiento: {score}")
    st.write("""El puntaje de sentimiento tiene un rango entre -1 y 1, siendo -1 muy negativo y 1 muy positivo, con una zona neutral
             entre -0.05 y 0.05. Para el puntaje anteriormente hallado, el sentimiento es: 
            """, sentiment(score))
    
st.markdown('***')
st.markdown("La clasificación de reseñas se ejecuta por medio del modelo [GPT 3.5 Turbo](https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates), mientras que el puntaje de sentimiento usa [VADER multilenguaje](https://github.com/brunneis/vader-multi) para su calculo.")