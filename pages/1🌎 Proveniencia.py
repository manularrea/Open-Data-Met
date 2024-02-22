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

department_check_box = st.checkbox('Filtrar por departamento del museo', value=False)
if department_check_box== True:
    department_options = st.multiselect(
    'Departamento de la obra',
    df_filtered['department'].unique().tolist(),
    ['Drawings and Prints'])
    df_filtered = apply_department_filter(df_filtered, department_options)




df_countries = df_filtered.groupby('country').size().reset_index(name='Número de piezas')




df_countries = df_countries.sort_values(by='Número de piezas', ascending=False)

col1, col2 = st.columns([3, 1])    

st.map(df_filtered)

expander = st.expander("Ver data")
expander.dataframe(df_countries, column_config = 
            {
                'country': 'País',
                'Número de piezas': 'Número de piezas adquiridas'
            },
            
    hide_index=True, use_container_width=True)


insight_expander = st.expander("Ver insight")
insight_expander.markdown("""
        
Desde su apertura en 1871 hasta 2023, el Met ha adquirido un total de 100,532 piezas de arte
de los Estados Unidos, lo que representa el mayor número de adquisiciones. De estas, el 24.7%
son de dominio público y el 75.3% están protegidas por derechos de au tor. Francia ocupa el
segundo lugar con 47,136 piezas, de las cuales el 43.7% son de dominio público y el 56.3% están
protegidas por derechos de autor. Egipto, con 30,940 piezas, tiene una distribución equitativa
entre las obras de dominio público y las pr otegidas por derechos de autor, cada una
representando el 50% del total. El Reino Unido e Italia siguen con 27,547 y 24,178 piezas
respectivamente, con una mayor proporción de obras de dominio público en Italia (53.1%) en
comparación con el Reino Unido (42.7%)

Al considerar solo las obras destacadas, los Estados Unidos lideran nuevamente con 593,
seguidos por Francia con 262 y Egipto con 124. Sin embargo, al considerar solo las obras no
destacadas, vemos un patrón similar con los Estados Unidos a la cabeza.
            
Estos datos indican que el Met tiene un interés particular en las obras de arte de los Estados
Unidos, tanto en el dominio público como protegidas por derechos de autor. Sin embargo,
también muestra un interés significativo en las obras de Francia, Egipto, Reino Unido e Italia.
En conclusión, los países que más interesan al Met, basándonos en el número de adquisiciones,
son los Estados Unidos, Francia, Egipto, el Reino Unido e Italia.
            """)



#------------------------------ SIDE BAR --------------------------------------
st.sidebar.markdown("---")
st.sidebar.header('Manuela Larrea Gómez')
st.sidebar.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.sidebar.write('Afi Escuela')
st.sidebar.write('Febrero, 2024')
