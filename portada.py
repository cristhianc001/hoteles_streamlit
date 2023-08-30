import streamlit as st
import transformers
from transformers import pipeline, tokenizers


st.image('https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png')
st.title('Introducción a Streamlit - Workshop')
st.markdown('***')

st.sidebar.markdown('Introducción sobre los usos y ventajas de Streamlit')


# @st.cache(hash_funcs={pipeline: lambda _: None, tokenizers.Tokenizer: lambda _: None})
def load_model():
    zsc_mDeBERTa = pipeline("zero-shot-classification", model = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7")
    return zsc_mDeBERTa
model = load_model()

candidate_labels = ["cleaning and bugs", "room and comfort", "staff and services", "food and drinks", "money"]


def zero_shot_classification(text, candidate_labels, model):
    results = model(text, candidate_labels)
    predicted_labels = []

    # Obtener la etiqueta con el puntaje más alto
    max_score_label = max(results['scores'])
    max_score_index = results['scores'].index(max_score_label)
    max_score_label = results['labels'][max_score_index]

    threshold = 0.3  # Umbral de confianza para considerar una etiqueta
    for label, score in zip(results['labels'], results['scores']):
        if score > threshold:
            predicted_labels.append(label)

    # Si ninguna etiqueta pasa el umbral, usar la etiqueta con el mayor score
    if not predicted_labels:
        predicted_labels.append(max_score_label)

    return predicted_labels

# Crear un cuadro de texto y obtener el texto ingresado por el usuario
input_text = st.text_input("Ingrese un texto:", value="Escribe aquí...")

# Verificar si el usuario ha ingresado texto y luego llamar a la función
if input_text:
    zero_shot_classification(input_text, candidate_labels, model)