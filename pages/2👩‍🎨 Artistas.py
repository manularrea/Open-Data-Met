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
    page_title="2. Artistas",
    page_icon="👩‍🎨",
)


# ------------- Side bar-------------------------------------------
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Metropolitan_Museum_of_Art_Logo.svg/2056px-The_Metropolitan_Museum_of_Art_Logo.svg.png"
image_2_url = 'https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/02/18171555/Met-logo.png'
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_2_url}" width="30%"></div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_url}" width="50%"></div>', unsafe_allow_html=True)
st.sidebar.title('The Metropolitan Museum of Art')
# -----------------------------------------------------------------------


st.title('2. ¿Qué artistas le interesan al MET?')

# Filtros globales para la data
exclude_unknown = st.checkbox('Excluir artistas anónimos o desconocidos', value=True) 
col1, col2= st.columns(2)
with col1:
    get_highlight =  st.radio('Mostrar obras:', ['Ambas','Destacadas', 'No Destacadas'])
with col2:
    get_license =  st.radio('Tipo de licencia de las obras:', ['Ambas', 'Dominio Público', 'Protegidas por derechos de autor'])


# Filtro del dataset según los filtros globales establecidos
df_filtered = apply_anonymous_filter(df, exclude_unknown, 'artistDisplayName')
df_filtered = apply_highlight_filter(df_filtered, get_highlight)
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

# Agrupa por artistDisplayName and artistNationality, y cuenta el número de piezas por artista.
artist_counts = df_filtered.groupby(['artistDisplayName', 'artistNationality']).size().reset_index(name='Piece Count')

# Organiza el dataset de mayor a menor
sorted_artists = artist_counts.sort_values(by='Piece Count', ascending=False)

# Obtiene el número de obras del 10 artista más popular, para luego filtrar el número de columnas a mostrar
min_piece_count = sorted_artists.iloc[10]['Piece Count']
print(min_piece_count)

# Filtrar los artists con un número menor al número mínimo establecido
artist_counts = artist_counts[artist_counts['Piece Count'] >= min_piece_count]

mean_accession_year_per_country = df_filtered.groupby('artistDisplayName')['accessionYear'].max().round(0).reset_index()
artist_counts = artist_counts.merge(mean_accession_year_per_country, on='artistDisplayName', how='left')




# GRÁFICO
bars = alt.Chart(artist_counts).mark_bar().encode(
    x=alt.X('Piece Count', axis=alt.Axis(title='Número de piezas')),
    y=alt.Y('artistDisplayName:N', sort='-x', axis=alt.Axis(title='Nombre del artista', labelFontSize=10)),  
    tooltip=[
        alt.Tooltip('artistDisplayName:N', title='Nombre del artista'),
        alt.Tooltip('artistNationality:N', title='Nacionalidad del artista'),
        alt.Tooltip('accessionYear:Q', title='Año de mayor adquisición'),
        alt.Tooltip('Piece Count:Q', title='Número de piezas')
    ]
).properties(
    title='Artistas de interés para el MET'
)

st.altair_chart(bars, theme='streamlit', use_container_width=True)



#------------------------------ SIDE BAR --------------------------------------
st.sidebar.markdown("---")
st.sidebar.header('Manuela Larrea Gómez')
st.sidebar.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.sidebar.write('Afi Escuela')
st.sidebar.write('Febrero, 2024')
