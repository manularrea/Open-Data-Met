import pandas as pd
import streamlit as st
import altair as alt


df = pd.read_csv('./data/cleaned_data.csv')
df = df.drop(columns=['Unnamed: 0'])

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Metropolitan_Museum_of_Art_Logo.svg/2056px-The_Metropolitan_Museum_of_Art_Logo.svg.png"
image_2_url = 'https://s3-eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2016/02/18171555/Met-logo.png'
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_2_url}" width="30%"></div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<div style="text-align:center;padding-bottom:10px;"><img src="{image_url}" width="50%"></div>', unsafe_allow_html=True)
st.sidebar.title('The Metropolitan Museum of Art')
st.sidebar.write('This is some information in the sidebar.')



# Add a checkbox to the sidebar for the global filter
exclude_unknown = st.sidebar.checkbox('Exclude Unknown Artists', value=True)
# Add a radio button to the sidebar for ordering
order_options = ['Ascending', 'Descending']
order = st.sidebar.radio('Order Bars by:', order_options)
# Add a number input to specify the maximum number of bars to show
max_bars = st.sidebar.number_input('Maximum Number of Bars', min_value=1, value=10)

# Qué artistas le interesan al MET?

def apply_global_filter(df, exclude_unknown):
    if exclude_unknown:
        df = df[df['artistDisplayName'] != 'Unknown']
    return df

# Filter the DataFrame based on the global filter
df_filtered = apply_global_filter(df, exclude_unknown)

# Filter the DataFrame to include only artists with at least 100 pieces
min_piece_count = 1
filtered_df = df_filtered.groupby('artistDisplayName').filter(lambda x: len(x) >= min_piece_count)

# Group by artistDisplayName and count the number of pieces for each artist
artist_counts = filtered_df['artistDisplayName'].value_counts()

# Filter out artists with less than min_piece_count pieces
artist_counts = artist_counts[artist_counts >= min_piece_count]

# Convert the Series back to a DataFrame
artist_counts_df = artist_counts.reset_index()
artist_counts_df.columns = ['Artist', 'Piece Count']

# Create a bar chart using Streamlit
st.title('Artists of Interest for the MET')
st.write('Select a minimum number of pieces to visualize:')
min_piece_count = st.slider('Minimum Piece Count:', min_value=1, max_value=4000, value=1)

# Filter the data based on the user's selection
filtered_artist_counts_df = artist_counts_df[artist_counts_df['Piece Count'] >= min_piece_count]

# Create a bar chart using Altair

# Sort the DataFrame based on the order option

if order == 'Ascending':
    artist_counts_df = artist_counts_df.sort_values(by='Piece Count', ascending=True)
    artist_counts_df = artist_counts_df.head(max_bars)
    bars = alt.Chart(artist_counts_df).mark_bar().encode(
        y='Piece Count',
        x=alt.X('Artist', sort='y'),  # Sort by Artist in descending order
        tooltip=['Artist', 'Piece Count']
    ).properties(
        title='Artists of Interest for the MET (Ascending)'
    )
else:
    artist_counts_df = artist_counts_df.sort_values(by='Piece Count', ascending=False)
    artist_counts_df = artist_counts_df.head(max_bars)
    bars = alt.Chart(artist_counts_df).mark_bar().encode(
        y='Piece Count',
        x=alt.X('Artist', sort='-y'),  # Sort by Artist in descending order
        tooltip=['Artist', 'Piece Count']
    ).properties(
        title='Artists of Interest for the MET (Descending)'
    )


st.altair_chart(bars, use_container_width=True)

st.sidebar.markdown("---")

st.sidebar.header('Manuela Larrea Gómez')
st.sidebar.write('Afi Escuela de Negocios')
st.sidebar.write('Máster en Data Science, Big Data e Inteligencia Artificial')
st.sidebar.write('Febrero, 2024')