

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Metropolitan Art Museum",
    page_icon="🎨",
)


### SIDEBAR ###

# Add a sidebar with information
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Metropolitan_Museum_of_Art_Logo.svg/2056px-The_Metropolitan_Museum_of_Art_Logo.svg.png"
image_2_url = 'https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/02/18171555/Met-logo.png'
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_2_url}" width="30%"></div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_url}" width="50%"></div>', unsafe_allow_html=True)
st.sidebar.title('The Metropolitan Museum of Art')

# Título
st.title("Visitando el Metropolitan Art Museum de NYC sin salir de Madrid")

st.image('https://cdn.sanity.io/images/cctd4ker/production/73a42b4ea1644b2085acaad2896bfa4699687664-2320x920.jpg?rect=405,0,1490,920&w=3840&q=75&fit=clip&auto=format')

# Descripción del proyecto
st.markdown("""

Este proyecto se basa en la política de datos abiertos del Museo Metropolitano de Arte de Nueva York (The Met) y utiliza su API para acceder a su vasta colección de obras de arte. En febrero de 2017, The Met lanzó su Iniciativa de Acceso Abierto, que permite el uso irrestricto de todas las imágenes de obras de arte de dominio público y datos básicos de todas las obras en su colección bajo la licencia Creative Commons Zero (CC0). Esto significa que cualquier persona puede descargar, compartir y remezclar imágenes y datos sobre las obras de arte en la colección de The Met.

El proyecto también se apoya en la API de Google Maps, que proporciona una amplia gama de servicios y herramientas para crear y optimizar aplicaciones basadas en la ubicación. Esta combinación permite visualizar la información de las obras de arte en un contexto geográfico, proporcionando una nueva dimensión a la exploración de la colección de The Met.
Finalmente, para desplegar la aplicación, se utiliza Streamlit.
            
""")

st.subheader('Objetivos del proyecto')

st.markdown("""
El proyecto se centra en responder las siguientes preguntas:
1.	¿De dónde provienen las obras de arte del Met?
2.	¿Cuáles son los artistas que más le interesan al Met?
3.	¿Cuáles son las culturas que más le interesan al Met?
4.	¿Cuál es el departamento del museo que tiene más piezas?
5.	¿Cuál es la evolución temporal del tamaño de la colección del Met?
6.	¿Cuáles son las obras más importantes del Met?
7.	¿Qué porción de las obras de arte del Met son de dominio público? 
            """)

# Pie de página
st.markdown("---")
st.write('Manuela Larrea Gómez')
st.write('Afi Escuela de Negocios')
st.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.write('Febrero, 2024')




st.sidebar.markdown("---")

