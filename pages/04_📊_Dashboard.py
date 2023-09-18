import streamlit as st

st.title('Dashboard de Power BI')
st.markdown('***')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintained by: Latam Data Consultores")

@st.cache_resource
def load_dashboard():
    iframe_code = """
    <iframe width="850" height="550" src="https://app.powerbi.com/view?r=eyJrIjoiMTZlNDBjZjItYTBiOC00NDk1LWEzNzUtNjY0OGZiODY3Zjg1IiwidCI6IjYzMmQzMWE5LWIxNWItNDgyNi05ZWQxLTUyYmRmZmI5YjdlNCIsImMiOjl9" frameborder="0" allowfullscreen="true"></iframe>
    """
    return st.markdown(iframe_code, unsafe_allow_html=True)

load_dashboard()

css = '''
<style>
    [data-testid='stSidebarNav'] > ul {
        min-height: 45vh;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)





# import streamlit as st

# # Define la métrica y su valor
# metric_name = "Ingresos Mensuales"
# metric_value = 8000  # Cambia este valor según tus necesidades
# objetivo = 10000

# # Calcula si se cumple el objetivo
# cumple_objetivo = metric_value >= objetivo

# # Define los colores para la tarjeta
# color_fondo = "green" if cumple_objetivo else "red"
# color_texto = "white" if cumple_objetivo else "black"

# # Aplica estilos CSS condicionales
# st.markdown(
#     f"""
#     <style>
#     .kpi-card {{
#         background-color: {color_fondo};
#         color: {color_texto};
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         font-size: 24px;
#     }}
#     </style>
#     """
#     ,
#     unsafe_allow_html=True,
# )

# # Crea la tarjeta KPI
# st.subheader("KPI Card")

# # Muestra el valor de la métrica y el estado del objetivo
# st.markdown(
#     f'<div class="kpi-card">**{metric_name}**: ${metric_value:,.2f} </div>', # ({"" if cumple_objetivo else "No "}Cumple Objetivo) para poner aviso entre parentesis
#     unsafe_allow_html=True,
# )
