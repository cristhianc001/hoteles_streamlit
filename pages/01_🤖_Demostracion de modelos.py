import streamlit as st
import openai
import re
import demoji
import openai

st.title('Demostración de clasificación de reseñas')
st.markdown('***')

openai.api_key = st.secrets["API_KEY"]

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

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

# Crear un cuadro de texto y obtener el texto ingresado por el usuario
input_text = st.text_input("Write a review:")

# Verificar si el usuario ha ingresado texto y luego llamar a la función
if input_text:
    input_text = cleaning_text(input_text)
    resultado =  get_completion(
        f""" 1. Give me the overall sentiment of the next review, the response can be pos for positive, neg for negative or neu for neutral.
            2. Give me the sentiment of the next categories of the review: room, guest service, cleaning and breakfast.
            The response must be pos for positive, neg for negative or neu neutral.
            3. The output must be in JSON format and the keys must be 'overall_sentiment', 'room_sentiment', 'guest_service_sentiment','cleaning_sentiment' and 'breakfast_sentiment'.
            \ ```{input_text}``` """)
        
    st.write("Sentiment Analysis:", resultado)