import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.filters import *

df = pd.read_feather('./data/clean_data.feather')
df = df.drop(columns=['Unnamed: 0'])

st.set_page_config(
    page_title="3. Culturas",
    page_icon="🗿",
)


# ------------- Side bar-------------------------------------------
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Metropolitan_Museum_of_Art_Logo.svg/2056px-The_Metropolitan_Museum_of_Art_Logo.svg.png"
image_2_url = 'https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/02/18171555/Met-logo.png'
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_2_url}" width="30%"></div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_url}" width="50%"></div>', unsafe_allow_html=True)
st.sidebar.title('The Metropolitan Museum of Art')
# -----------------------------------------------------------------------


st.title('3. ¿Cuáles son las culturas más representadas en las obras que se encuentran en el Met?')

# Filtros globales para la data
exclude_unknown = st.checkbox('Excluir culturas desconocidas', value=True) 
col1, col2= st.columns(2)
with col1:
    get_highlight =  st.radio('Mostrar obras:', ['Ambas','Destacadas', 'No Destacadas'])
with col2:
    get_license =  st.radio('Tipo de licencia de las obras:', ['Ambas', 'Dominio Público', 'Protegidas por derechos de autor'])

# Filtro del dataset según los filtros globales establecidos
df_filtered = apply_anonymous_filter(df, exclude_unknown, 'culture')
df_filtered = apply_highlight_filter(df_filtered, get_highlight)
df_filtered = apply_license_filter(df_filtered, get_license)

accession_years = df_filtered['accessionYear'].unique().tolist()
accession_years = [x for x in accession_years if isinstance(x, int)]
adquisicion_slider =st.slider('Año mínimo de adquisición:', min_value=min(accession_years), max_value=max(accession_years), value=min(accession_years))
df_filtered = apply_accession_filter(df_filtered, adquisicion_slider)

    
culture_count = df_filtered.groupby(['culture']).size().reset_index(name='Número de Piezas')

# Organiza el dataset de mayor a menor
sorted_cultures = culture_count.sort_values(by='Número de Piezas', ascending=False)

# Obtiene el número de obras del 10 artista más popular, para luego filtrar el número de columnas a mostrar
min_piece_count = sorted_cultures.iloc[10]['Número de Piezas']
print(min_piece_count)

# Filtrar los artists con un número menor al número mínimo establecido
culture_count = culture_count[culture_count['Número de Piezas'] >= min_piece_count]

# GRÁFICO
bars = alt.Chart(culture_count).mark_bar().encode(
    x=alt.X('Número de Piezas', axis=alt.Axis(title='Número de piezas')),
    y=alt.Y('culture:N', sort='-x', axis=alt.Axis(title='Cultura', labelFontSize=10)),  
    tooltip=[
        alt.Tooltip('culture:N', title='Cultura'),
    ]
).properties(
    title='Culturas de las obras del MET'
)

st.altair_chart(bars, theme='streamlit', use_container_width=True)


insight_expander = st.expander("Ver insight")
insight_expander.markdown("""

Los resultados sugieren que la cultura Americana es de gran interés para el
Met en varios aspectos. En la colección general del museo, la cultura Americana tiene la mayor cantidad de
piezas. Incluso cuando se consideran solo las obras destacadas, la cultura Americana sigue
siendo la más prominente.
                          
Además, en la colección de obras protegidas por derechos de autor, la cultura Americana también
es la más representada. Sin embargo, cuando se trata de obras de dominio público, la cultura
Griega Ática es la más prominente.
                          
Por lo tanto, aunque la cultura Americana parece ser la que más interesa al Met en términos
generales y en obras destacadas y protegidas por derechos de autor, la cultura Griega Ática es
la más prominente en términos de obras de dominio público. Esto sugie re que el Met tiene un
interés diversificado en diferentes culturas dependiendo del tipo de obras que se consideren.
            """)

#------------------------------ SIDE BAR --------------------------------------
st.sidebar.markdown("---")
st.sidebar.header('Manuela Larrea Gómez')
st.sidebar.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.sidebar.write('Afi Escuela')
st.sidebar.write('Febrero, 2024')
