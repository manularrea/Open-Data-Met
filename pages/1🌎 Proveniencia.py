import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.filters import *

df = pd.read_feather('./data/clean_data.feather')
df = df.drop(columns=['Unnamed: 0'])

df.dropna(subset=['lat', 'lon'], inplace=True)

st.set_page_config(
    page_title="1. Proveniencia",
    page_icon="🌎",
)


# ------------- Side bar-------------------------------------------
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Metropolitan_Museum_of_Art_Logo.svg/2056px-The_Metropolitan_Museum_of_Art_Logo.svg.png"
image_2_url = 'https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/02/18171555/Met-logo.png'
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_2_url}" width="30%"></div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_url}" width="50%"></div>', unsafe_allow_html=True)
st.sidebar.title('The Metropolitan Museum of Art')
# -----------------------------------------------------------------------


st.title('1. ¿De dónde provienen las obras de arte del MET?')

# Filtros globales para la data

col1, col2= st.columns(2)
with col1:
    get_highlight =  st.radio('Mostrar obras:', ['Destacadas', 'No Destacadas', 'Ambas'])
with col2:
    get_license =  st.radio('Tipo de licencia de las obras:', ['Dominio Público', 'Protegidas por derechos de autor', 'Ambas'])

# Filtro del dataset según los filtros globales establecidos
df_filtered = apply_highlight_filter(df, get_highlight)
df_filtered = apply_license_filter(df_filtered, get_license)

accession_years = df_filtered['accessionYear'].unique().tolist()
accession_years = [x for x in accession_years if isinstance(x, int)]
adquisicion_slider =st.slider('Año mínimo de adquisición:', min_value=min(accession_years), max_value=max(accession_years), value=min(accession_years))
df_filtered = apply_accession_filter(df_filtered, adquisicion_slider)

department_check_box = st.checkbox('Filtrar por departamento', value=False)
if department_check_box== True:
    department_options = st.multiselect(
    'Departamento de la obra',
    df_filtered['department'].unique().tolist(),
    ['Drawings and Prints'])
    df_filtered = apply_department_filter(df_filtered, department_options)




df_countries = df_filtered.groupby('country').size().reset_index(name='Número de piezas')
accession_years_graph = df_filtered.groupby('country')['accessionYear'].agg(list).reset_index()



# Merge the mean accession year data with the original DataFrame
df_countries = df_countries.merge(accession_years_graph, on='country', how='left')

df_countries = df_countries.sort_values(by='Número de piezas', ascending=False)

col1, col2 = st.columns([3, 1])    

st.map(df_filtered)

expander = st.expander("Ver data")
expander.dataframe(df_countries, column_config = 
            {
                'country': 'País',
                "accessionYear_y": st.column_config.LineChartColumn(
                "Años de adquisición", y_min=min(accession_years), y_max=max(accession_years)
        ),
            },
            
    hide_index=True, use_container_width=True)





#------------------------------ SIDE BAR --------------------------------------
st.sidebar.markdown("---")
st.sidebar.header('Manuela Larrea Gómez')
st.sidebar.write('Afi Escuela de Finanzas')
st.sidebar.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.sidebar.write('Febrero, 2024')
