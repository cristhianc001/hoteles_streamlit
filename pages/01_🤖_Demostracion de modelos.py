########### LIBRERIAS
import pandas as pd
import ast
import random
import streamlit as st
import openai
import re
import time
import demoji
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

########### TITULO
st.title('Demostración de clasificación de reseñas')
st.markdown('***')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintained by: Latam Data Consultores")

########### VARIABLES Y FUNCIONES
openai.api_key = st.secrets["API_KEY"]

@st.cache_data
def load_data():
    df = pd.read_parquet("data/reviews-model.parquet")
    return df
df = load_data()

@st.cache_resource
def load_analyzer():
  return SentimentIntensityAnalyzer()

analyzer = load_analyzer()

@st.cache_resource
def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
      messages = [{"role": "user", "content": prompt}]
      response = openai.ChatCompletion.create(
          model=model,
          messages=messages,
          temperature=0, # this is the degree of randomness of the model's output
      )
      return response.choices[0].message["content"]
    except openai.error.RateLimitError as e:      
        return st.error("Limite excedido. Intente de nuevo más tarde.")

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
         por medio de reseñas individuales introducidas en el cuadro de texto al final de la página.""")

st.write("""El resultado de sentimiento por categoria se divide por 'pos' siendo positivo, 'neu' neutral y 'neg' negativo. 
            Ademas de su categorización por servicios del hotel: estado de la habitación, atención al cliente, limpieza y desayuno.
            """)

st.markdown(
    """<div style='background-color: purple; padding: 10px; color: white; border-radius: 10px;'>
       La clasificación de reseñas se ejecuta por medio del modelo <a href='https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates' style='color: white;'>GPT 3.5 Turbo</a>,
       mientras que el puntaje de sentimiento usa <a href='https://github.com/brunneis/vader-multi' style='color: white;'>VADER multilenguaje</a> para su cálculo.
       </div>""",
    unsafe_allow_html=True
)

st.markdown('***')

random_index = random.randint(0, len(df) - 1)
random_review = df.loc[random_index, "review"]
st.markdown("***Reseña Aleatoria***:")
st.info(random_review)

# Crear un cuadro de texto y obtener el texto ingresado por el usuario
input_text = st.text_input("Escribe una reseña aqui o prueba la aleatoria:")

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
    st.success("### Sentimiento por categoria")
    st.dataframe(df)
     
    st.success(f"### Puntaje de sentimiento: {score}")
    st.markdown(f"""El puntaje de sentimiento tiene un rango entre -1 y 1, siendo -1 muy negativo y 1 muy positivo, con una zona neutral
             entre -0.05 y 0.05. Para el puntaje anteriormente hallado, el sentimiento es: 
            *{sentiment(score)}* """)
  

css = '''
<style>
    [data-testid='stSidebarNav'] > ul {
        min-height: 45vh;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)
    

