import streamlit as st

st.title('Acerca de nosotros')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintained by: Latam Data Consultores")

@st.cache_resource
def load_image():
    return st.image('https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/team.png')
load_image()

st.info("""
        ***Data Analyst***: [Douglas Sanchez](https://www.linkedin.com/in/douglassanchezcasanova/)
        
        ***Data Engineers***: [Yaneth Ramirez]( https://www.linkedin.com/in/yanethramirez/), [Hugo Salazar](https://www.linkedin.com/in/hasalazars/)
        
        ***Data Scientists***: [Cristhian Castro](https://www.linkedin.com/in/cristhiancastro/), [Rodrigo Moreira](https://www.linkedin.com/in/rcmoreg)

        ***Repositorio del Proyecto***: [Github](https://github.com/cristhianc001/Analisis-Sentimientos-Hoteles)

        """)


css = '''
<style>
    [data-testid='stSidebarNav'] > ul {
        min-height: 45vh;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)