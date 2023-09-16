import streamlit as st

# st.title('Sistema de Analisis de Reseñas')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintaned by: Latam Data Consultores")

@st.cache_resource
def load_portrait():
    return st.image('https://raw.githubusercontent.com/cristhianc001/Analisis-Sentimientos-Hoteles/main/img/1.jpg')
load_portrait()

st.markdown('***')
# st.image('https://1000marcas.net/wp-content/uploads/2021/06/Ramada-logo.png')
# st.image('https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/ramada_logo.png')

@st.cache_resource
def load_video():
    return st.video("https://www.youtube.com/watch?v=t-39RZ5zcLo")
load_video()

# PARA VER TODAS LAS TABS DE LA IZQUIERDA, ENTRE MAS vh MAS AMPLIO ES
css = '''
<style>
    [data-testid='stSidebarNav'] > ul {
        min-height: 45vh;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)
