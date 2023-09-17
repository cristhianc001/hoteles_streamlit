import streamlit as st

st.title('Dashboard de Power BI')
st.markdown('***')
st.sidebar.image("https://raw.githubusercontent.com/cristhianc001/hoteles_streamlit/main/img/icon.png",caption="Developed and Maintained by: Latam Data Consultores")

@st.cache_resource
def load_dashboard():
    iframe_code = """
    <iframe width="800" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiMTZlNDBjZjItYTBiOC00NDk1LWEzNzUtNjY0OGZiODY3Zjg1IiwidCI6IjYzMmQzMWE5LWIxNWItNDgyNi05ZWQxLTUyYmRmZmI5YjdlNCIsImMiOjl9" frameborder="0" allowfullscreen="true"></iframe>
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
