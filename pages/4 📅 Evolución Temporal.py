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
    page_title="4. Evolución Temporal",
    page_icon="📅",
)


# ------------- Side bar-------------------------------------------
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Metropolitan_Museum_of_Art_Logo.svg/2056px-The_Metropolitan_Museum_of_Art_Logo.svg.png"
image_2_url = 'https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/02/18171555/Met-logo.png'
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_2_url}" width="30%"></div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_url}" width="50%"></div>', unsafe_allow_html=True)
st.sidebar.title('The Metropolitan Museum of Art')
# -----------------------------------------------------------------------


st.title('4. ¿Cuál es la evolución temporal del tamaño de la colección del Met?')

# Filtros globales para la data
col1, col2= st.columns(2)
with col1:
    get_highlight =  st.radio('Mostrar obras:', ['Ambas','Destacadas', 'No Destacadas'])
with col2:
    get_license =  st.radio('Tipo de licencia de las obras:', ['Ambas', 'Dominio Público', 'Protegidas por derechos de autor'])

# Filtro del dataset según los filtros globales establecidos
df_filtered = apply_highlight_filter(df, get_highlight)
df_filtered = apply_license_filter(df_filtered, get_license)

accession_years = df_filtered['accessionYear'].unique().tolist()
accession_years = [x for x in accession_years if isinstance(x, int)]
adquisicion_slider =st.slider('Año mínimo de adquisición:', min_value=min(accession_years), max_value=max(accession_years), value=min(accession_years))
df_filtered = apply_accession_filter(df_filtered, adquisicion_slider)

department_check_box = st.checkbox('Filtrar por departamento del museo', value=False)
if department_check_box== True:
    container = st.container()
    col1, col2 = container.columns([3, 1])
    all = col2.checkbox("Seleccionar todos los departamentos")
    department_list = df_filtered['department'].unique().tolist()
    if all:
        department_options = col1.multiselect(
        'Departamento de la obra',
        department_list,
        department_list)
    else:
        department_options = col1.multiselect(
        'Departamento de la obra',
        df_filtered['department'].unique().tolist(),
        ['Drawings and Prints'])
    df_filtered = apply_department_filter(df_filtered, department_options)

years_count = df_filtered.groupby(['accessionYear', 'department']).size().reset_index(name='Número de Piezas')

if department_check_box== True:
    if isinstance(department_options, list):
        chart = alt.Chart(years_count).mark_line().encode(
            x=alt.X('accessionYear:O', title='Año de adquisición'),
            y='Número de Piezas:Q',
            color = alt.Color("department", title='Departamento') 
        ).properties(
            width=500,
            height=300
        )
else:
    chart = alt.Chart(years_count).mark_line().encode(
        x=alt.X('accessionYear:O', title='Año de adquisición'),
        y='Número de Piezas:Q'
    ).properties(
        width=500,
        height=300
    )


st.altair_chart(chart, use_container_width=True)

insight_expander = st.expander("Ver insight")
insight_expander.markdown("""
La evolución temporal del tamaño de la colección del Met muestra un incremento constante en
el volumen de obras, marcado por picos muy puntuales de adquisición. Desde su fundación, el
museo ha mantenido una tendencia al aumento gradual. Un punto de inflexión significativo se
registró después de 1962, cuando la colección general experimentó un aumento notable con la adquisición de más de 40000 piezas. Sin embargo,
al analizar destacadas y no destacadas, los picos están ubicados en distintos años.
                          
Las obras destacadas revelaron un pico de adquisición posterior a 1974, con cerca de 100 piezas
adicionales. Por otro lado, las obras no destacadas alcanzaron su punto máximo de adquisición
también en 1962, con casi 40000 piezas . Las obras de dominio público exhiben dos picos
notables después de 1962 y posterior al 2010, con adquisiciones superiores a las 16000 piezas
en ambos casos. Mientras tanto, las obras protegidas por derechos de autor muestran tres picos,
el primero tras 1 962 con más de 20,000 piezas , seguido en 1994 con más de 7000, y nuevamente
en 2010 con más de 5000 piezas.
                          
Estos hitos evidencian la complejidad en la evolución de la colección del Met, donde los
momentos de intenso crecimiento podrían sugerir cambios en las políticas curatoriales y
enfoques de selección a lo largo de los años.
            """)
#------------------------------ SIDE BAR --------------------------------------
st.sidebar.markdown("---")
st.sidebar.header('Manuela Larrea Gómez')
st.sidebar.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.sidebar.write('Afi Escuela')
st.sidebar.write('Febrero, 2024')
