########### LIBRERIAS

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

########### TITULO
st.title('Visualización Geografica')
st.markdown('***')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintained by: Latam Data Consultores")
st.info("Posa el cursor sobre el icono seleccionado y podrás obtener algunos indicadores del hotel.")

########### VARIABLES Y FUNCIONES
@st.cache_data
def load_lodgings():
    df_lodgings = pd.read_parquet("data/df_lodgings.parquet") # cargar df de hoteles
    return df_lodgings

@st.cache_data
def load_reviews():
    df_reviews = pd.read_parquet("data/reviews-model.parquet") # cargar df de reseñas
    return df_reviews

@st.cache_data
def data_merge(df1, df2, column): # merge df de hoteles y reseñas
    df_merged = df1.merge(df2, on=column)
    return df_merged

@st.cache_data
def percentage_pos(df): # cargar df con porcentaje de reviews positivas por hotel
    reviews_pos = df[df['rating'] > 3]
    perc_pos = reviews_pos.groupby(["lodging_id", "lodging_name"])['rating'].count() / df.groupby(["lodging_id", "lodging_name"])['rating'].count() * 100
    df_perc_pos = pd.DataFrame({'perc_pos': perc_pos})
    df_perc_pos = df_perc_pos.reset_index()
    return df_perc_pos

@st.cache_data
def percentage_neg(df): # cargar df con porcentaje de reviews negativas por hotel
    reviews_neg = df[df['rating'] < 3]
    perc_neg = reviews_neg.groupby(["lodging_id", "lodging_name"])['rating'].count() / df.groupby(["lodging_id", "lodging_name"])['rating'].count() * 100
    df_perc_neg = pd.DataFrame({'perc_neg': perc_neg})
    df_perc_neg = df_perc_neg.reset_index()
    return df_perc_neg

@st.cache_data
def data_grouped(df, df1, df2):  # agrupar df para calcular promedio de rating y sentimiento por hotel, luego merge con los df de porcentaje
    df_grouped = df.groupby(["lodging_id", "lodging_name"]).agg(
    avg_rating=("rating", "mean"),
    avg_sentiment=("sentiment_score", "mean")
    ).reset_index()

    df_grouped = df_grouped.merge(df1, on=["lodging_id", "lodging_name"]).merge(df2, on=["lodging_id", "lodging_name"])
    df_grouped["avg_rating"] = df_grouped["avg_rating"].round(3)
    df_grouped["avg_sentiment"] = df_grouped["avg_sentiment"].round(3)
    df_grouped["perc_pos"] = df_grouped["perc_pos"].round(3)
    df_grouped["perc_neg"] = df_grouped["perc_neg"].round(3)
    return df_grouped
    
df_lodgings = load_lodgings()
df_reviews = load_reviews()
df_merged = data_merge(df_reviews, df_lodgings, "lodging_id")
df_perc_pos = percentage_pos(df_merged)
df_perc_neg = percentage_neg(df_merged)
df_grouped = data_grouped(df_merged, df_perc_pos, df_perc_neg)

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
                            <b>Sentimiento Promedio:</b> {row['avg_sentiment']}<br>
                            <b>% Positivas (Rating):</b> {row['perc_pos']}<br> 
                            <b>% Negativas (Rating):</b> {row['perc_neg']}""",  # tooltip para que muestre datos cuando se pose
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
                            <b>Sentimiento Promedio:</b> {row['avg_sentiment']}<br>
                            <b>% Positivas (Rating):</b> {row['perc_pos']}<br> 
                            <b>% Negativas (Rating):</b> {row['perc_neg']}""" 
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

st.warning("El porcentaje de reviews positivas y negativas se calculó de acuerdo al rating. Se considera un rating mayor a 3 como positivo, un rating menor a 3 como negativo e igual a 3 como neutro.")

css = '''
<style>
    [data-testid='stSidebarNav'] > ul {
        min-height: 45vh;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)


