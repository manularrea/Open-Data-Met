import requests
import json

def get_objects_id():
    # Send a GET request to the API
    response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects')
    # Check if the request was successful
    if response.status_code == 200:
        # Return the object IDs
        return response.json()['objectIDs']
    else:
        return None

def get_object_by_id(object_id):
    # Send a GET request to the API using the object_id parameter
    response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}')
    # Check if the request was successful
    if response.status_code == 200:
        # Return the object data
        return response.json()
    else:
        return None

def save_object_data(object_data, filename):
    # Save the object data to a JSON file
    with open(filename, 'w') as f:
        json.dump(object_data, f, indent=4)

def save_data_to_json_file(filename):
    i=0
    object_ids = get_objects_id()
    if object_ids:
        all_object_data = []
        for object_id in object_ids:
            object_data = get_object_by_id(object_id)
            if object_data:
                all_object_data.append(object_data)
                # Chequeo de el progreso de la descarga de datos.
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
    with open('./utils/api_key.txt', 'r') as file:
        return file.read().strip()

api_key = get_api_key()

def get_lat_lng(country):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={country}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        location = data['results'][0]['geometry']['location']
        print('Got data')
        return location['lat'], location['lng']
    else:
        return None, None  

def get_country(country):
    country = country.str.replace(" ", '%20')
    url = f'https://restcountries.com/v3.1/name/{country}'
    response = requests.get(url)
    data = response.json()
    if response.status_code==200:
        country = data[0]['name']['common']
        print(country)
        return country
    else:
        return country    
