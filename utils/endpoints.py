# Este script proporciona funciones para interactuar con dos APIs diferentes: el Museo Metropolitano de Nueva York y Google Maps.

import requests
import json

#----------------------------------------------------------------------------------------------------------------------
# API del Museo Metropolitano de Nueva York 
#----------------------------------------------------------------------------------------------------------------------
def get_objects_id():
    # Envía una solicitud GET a la API 
    response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects')
    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Devuelve los IDs de los objetos
        return response.json()['objectIDs']
    else:
        return None

def get_object_by_id(object_id):
    # Envía una solicitud GET a la API utilizando el parámetro object_id
    response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}')
    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Devuelve los datos del objeto
        return response.json()
    else:
        return None

def save_object_data(object_data, filename):
    # Guardo los datos del objeto en un archivo JSON
    with open(filename, 'w') as f:
        json.dump(object_data, f, indent=4)

# Función para guardar todos los datos de los objetos en un archivo JSON
def save_data_to_json_file(filename):
    i=0
    object_ids = get_objects_id()
    if object_ids:
        all_object_data = []
        for object_id in object_ids:
            object_data = get_object_by_id(object_id)
            if object_data:
                all_object_data.append(object_data)
                # Con este contador chequeo el progreso de la descarga de datos.
                i=i+1
                print(f'{i}. Got object data for ID {object_id}')
            else:
                print(f"Failed to get object data for ID {object_id}, {i}")

        if all_object_data:
            print(f"Object data saved to {filename}")
            save_object_data(all_object_data, filename)
        else:
            print("Failed to get any object data.")
    else:
        print("Failed to get object IDs.")
        
def get_api_key():
    # Abre y lee el archivo que contiene la clave de la API 
    # Esto lo hago por seguridad, para que no me queden claves expuestas en el repo remoto (incluído en el .gitignore).
    with open('./utils/api_key.txt', 'r') as file:
        return file.read().strip()

api_key = get_api_key()

# ---------------------------------------------------------------------------------------------------
# API de Google Maps para información de georreferenciación
# ---------------------------------------------------------------------------------------------------

# Función para obtener las coordenadas de latitud y longitud de un país
def get_lat_lng(country):
    # Construye la URL para la solicitud GET a la API
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={country}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Se crea esta excepcion para controlar errores. Si se produce alguno, devuelve None.
        try:
            # Extrae la latitud y longitud de la respuesta
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        except:
            return None, None
    else:
        return None, None  

