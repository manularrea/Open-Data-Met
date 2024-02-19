

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
st.title("Bienvenido al Proyecto MET")

st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Metropolitan_Museum_of_Art_%28The_Met%29_-_Central_Park%2C_NYC.jpg/1200px-Metropolitan_Museum_of_Art_%28The_Met%29_-_Central_Park%2C_NYC.jpg')

# Descripción del proyecto
st.markdown("""

El Metropolitan Museum of Art (MET), una institución cultural de renombre internacional, se erige como un bastión del arte y la historia, albergando una colección que abarca desde la antigüedad hasta el arte contemporáneo.

El Museo Metropolitano de Arte presenta más de 5000 años de arte de todo el mundo para que todos puedan experimentar y disfrutar. El Museo está ubicado en dos sitios emblemáticos de la ciudad de Nueva York: The Met Fifth Avenue y The Met Cloisters. Millones de personas también participan en la experiencia The Met en línea.

Desde su fundación en 1870, el Met siempre ha aspirado a ser más que un tesoro de objetos raros y hermosos. Cada día, el arte cobra vida en las galerías del Museo y a través de sus exposiciones y eventos, revelando nuevas ideas y conexiones inesperadas a través del tiempo y de las culturas.

El Museo Metropolitano de Arte proporciona conjuntos de datos selectos de información sobre más de 470.000 obras de arte de su colección para uso comercial y no comercial sin restricciones. 

Los conjuntos de datos de acceso abierto del Met están disponibles a través de su API.  Este proyecto se propone aprovecharla para obtener datos exhaustivos sobre la colección de arte del Museo, y responder las siguientes preguntas: 

1. ¿De dónde provienen las obras de arte del MET?
2. ¿Qué artistas le interesan al MET?
3. ¿Qué departamento tiene el mayor número de piezas?
4. ¿Qué culturas le interesan al MET?
5. ¿Cuáles son los materiales más usados en las obras de arte que se encuentran en el MET?
6. ¿Cuál es la evolución temporal del número de obras en la colección del MET?
7. ¿Cuáles son las obras más importantes del MET?
8. ¿Qué porción de las obras de arte del MET son de dominio público?

""")


# Pie de página
st.markdown("---")
st.write('Manuela Larrea Gómez')
st.write('Afi Escuela de Negocios')
st.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.write('Febrero, 2024')




st.sidebar.markdown("---")

