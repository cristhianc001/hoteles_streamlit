import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.title('Visualización Geografica')
st.markdown('***')

@st.cache_data
def load_lodgings():
    df_lodgings = pd.read_parquet("data/df_lodgings.parquet")
    return df_lodgings

df_lodgings = load_lodgings()

# Lista de opciones para la lista desplegable
opciones = ["Nacional"]

opcion_seleccionada = st.selectbox("Selecciona una opción:", opciones)

if opcion_seleccionada == "Nacional":
    # Crear un clúster de marcadores para hoteles seleccionados
    mc_selected = MarkerCluster()
    mc_unselected = MarkerCluster()

    map_center = [df_lodgings['latitude'].mean(), df_lodgings['longitude'].mean()]

    m_3 = folium.Map(location=map_center, tiles='cartodbpositron', zoom_start=4.5)

    for idx, row in df_lodgings.iterrows():
        if not pd.isna(row['longitude']) and not pd.isna(row['latitude']):
            # Verificar si el hotel está en la lista de hoteles seleccionados
            if row['lodging_name'] in opciones:
                # Agregar un marcador con estilo diferente para hoteles seleccionados
                marcador = folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    tooltip=row['lodging_name'],  # tooltip para que muestre el nombre cuando se pose
                    icon=folium.Icon(color='red', icon='info-sign')  # Cambia el color del icono a rojo
                )
                marcador.add_to(mc_selected)
            else:
                # Agregar un marcador normal para hoteles no seleccionados
                marcador = folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    tooltip=row['lodging_name']  # tooltip para que muestre el nombre cuando se pose
                )
                marcador.add_to(mc_unselected)

    # Agregar los clústeres de marcadores al mapa principal
    m_3.add_child(mc_selected)
    m_3.add_child(mc_unselected)

    st.markdown("### Mapa de hoteles")
    st.write("Haga clic en los marcadores para obtener información.")
    folium_static(m_3)
