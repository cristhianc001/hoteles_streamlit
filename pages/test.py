########### LIBRERIAS

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

########### TITULO
st.title('Visualización Geografica')
st.markdown('***')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintaned by: Latam Data Consultores")

########### VARIABLES Y FUNCIONES
@st.cache_data
def load_lodgings():
    df_lodgings = pd.read_parquet("data/df_lodgings.parquet")
    return df_lodgings
@st.cache_data
def load_reviews():
    df_reviews = pd.read_parquet("data/reviews-model.parquet")
    return df_reviews
@st.cache_data
def data_merge(df1, df2, column):
    df_merged = df1.merge(df2, on=column)
    return df_merged

df_lodgings = load_lodgings()
df_reviews = load_reviews()
df_merged = data_merge(df_reviews, df_lodgings, "lodging_id")

df_grouped = df_merged.groupby(["lodging_id", "lodging_name"]).agg(
    avg_rating=("rating", "mean"),
    avg_sentiment=("sentiment_score", "mean")
).reset_index()

df_grouped["avg_rating"] = df_grouped["avg_rating"].round(3)
df_grouped["avg_sentiment"] = df_grouped["avg_sentiment"].round(3)


# Hotels de competencia
lista_id_NV = [811,855,851]
lista_id_FL = [1076,1010,1062]
lista_id_CA = [1159,1164,1175,1653]
lista_id_NY = [1725,1328,1366,1356]
lista_id_TX = [1520,1521,1517]

# Lista de opciones para la lista desplegable
opciones = ["Nacional", "Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive", "Ramada by Wyndham New York Times Square West",
            "Ramada Plaza by Wyndham West Hollywood Hotel & Suites",  "Ramada by Wyndham Reno Hotel & Casino", 
            "Ramada by Wyndham Houston Intercontinental Airport East"]

def map(df, zoom):
     # Crear un clúster de marcadores para hoteles seleccionados
    mc_selected = MarkerCluster()
    mc_unselected = MarkerCluster()

    map_center = [df['latitude'].mean(), df['longitude'].mean()]

    m_3 = folium.Map(location=map_center, tiles='cartodbpositron', zoom_start=zoom)

    for idx, row in df.iterrows():
        if not pd.isna(row['longitude']) and not pd.isna(row['latitude']):
            # Verificar si el hotel está en la lista de hoteles seleccionados
            if row['lodging_name'] in opciones: # Si el nombre del hotel esta dentro de las opciones desplegables
                # Agregar un marcador con estilo diferente
                marcador = folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    tooltip= f"""
                            <b>Nombre del Hotel:</b> {row['lodging_name']}<br>
                            <b>Rating Promedio:</b> {row['avg_rating']}<br>
                            <b>Sentimiento Promedio:</b> {row['avg_sentiment']}""",  # tooltip para que muestre datos cuando se pose
                    icon=folium.Icon(color='red', icon='info-sign')  # Cambia el color del icono a rojo
                )
                marcador.add_to(mc_selected)
            else:
                # Agregar un marcador normal para hoteles no seleccionados (la competencia)
                marcador = folium.Marker(
                    location = [row['latitude'], row['longitude']],
                    tooltip = f"""
                            <b>Nombre del Hotel:</b> {row['lodging_name']}<br>
                            <b>Rating Promedio:</b> {row['avg_rating']}<br>
                            <b>Sentimiento Promedio:</b> {row['avg_sentiment']}""" 
                )
                marcador.add_to(mc_unselected)

    # Agregar los clústeres de marcadores al mapa principal
    m_3.add_child(mc_selected)
    m_3.add_child(mc_unselected)

    st.markdown("### Mapa de hoteles")
    return folium_static(m_3)

########### CONTENIDO
opcion_seleccionada = st.selectbox("Selecciona una opción:", opciones)
hoteles = []
# Hoteles de Ramada
if opcion_seleccionada == "Ramada by Wyndham Reno Hotel & Casino":
    hoteles = lista_id_NV
elif opcion_seleccionada == "Ramada Plaza by Wyndham Orlando Resort & Suites Intl Drive":
    hoteles = lista_id_FL
elif opcion_seleccionada == "Ramada Plaza by Wyndham West Hollywood Hotel & Suites":
    hoteles = lista_id_CA
elif opcion_seleccionada == "Ramada by Wyndham New York Times Square West":
    hoteles = lista_id_NY
elif opcion_seleccionada == "Ramada by Wyndham Houston Intercontinental Airport East":
    hoteles = lista_id_TX
elif opcion_seleccionada == "Nacional":
    hoteles = lista_id_NV + lista_id_FL + lista_id_CA + lista_id_NY + lista_id_TX

df_filtrado = df_lodgings[df_lodgings['lodging_id'].isin(hoteles)]
df = df_filtrado.merge(df_grouped, on=["lodging_id", "lodging_name"])

map(df, 4)


