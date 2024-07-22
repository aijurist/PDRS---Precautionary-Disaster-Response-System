import ee
from flask import Blueprint, jsonify, request
from google.oauth2 import service_account
from flask_cors import CORS
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import requests
from location_finder import location_model

load_dotenv()

SERVICE_ACCOUNT_KEY = os.getenv('SERVICE_ACCOUNT_KEY')
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_KEY,
    scopes=['https://www.googleapis.com/auth/earthengine']
)

ee.Initialize(credentials)

validation = Blueprint('validation', __name__)
geolocator = Nominatim(user_agent="hackfest_2024")

def split_population(population, urban=True):
    children_ratio = 0.30
    adults_18_44_ratio = 0.40
    adults_45_59_ratio = 0.20
    adults_60_plus_ratio = 0.10

    children = population * children_ratio
    adults_18_44 = population * adults_18_44_ratio
    adults_45_59 = population * adults_45_59_ratio
    adults_60_plus = population * adults_60_plus_ratio

    if urban:
        male_ratio = 1000 / (1000 + 929)
        female_ratio = 929 / (1000 + 929)
    else:
        male_ratio = 1000 / (1000 + 949)
        female_ratio = 949 / (1000 + 949)

    male_population = population * male_ratio
    female_population = population * female_ratio

    return {
        'children': int(children),
        'adults_18_44': int(adults_18_44),
        'adults_45_59': int(adults_45_59),
        'adults_60_plus': int(adults_60_plus),
        'male_population': int(male_population),
        'female_population': int(female_population)
    }

@validation.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    try:
        data = request.json
        location_name = data.get('location_name')

        if not location_name:
            return jsonify({
                'status': 'error',
                'message': 'Location name must be provided'
            })

        location = geolocator.geocode(location_name)
        if location:
            return jsonify({
                'status': 'success',
                'location_name': location_name,
                'latitude': location.latitude,
                'longitude': location.longitude
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Could not find coordinates for the given location name'
            })

    except GeocoderServiceError as e:
        return jsonify({
            'status': 'error',
            'message': f'Geocoding service error: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@validation.route('/get_population', methods=['POST'])
def get_population():
    try:
        data = request.json
        lat = data.get('lat')
        lon = data.get('lon')
        location_name = data.get('location_name')
        radius = data['radius']
        is_urban = data['is_urban']

        if not lat or not lon:
            if location_name:
                response = requests.post('http://127.0.0.1:8080/api_validation/get_coordinates', json={'location_name': location_name})
                if response.status_code == 200:
                    coordinates_data = response.json()
                    if coordinates_data['status'] == 'success':
                        lat = coordinates_data['latitude']
                        lon = coordinates_data['longitude']
                    else:
                        return jsonify({
                            'status': 'error',
                            'message': 'Could not get coordinates from location name'
                        })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Error in getting coordinates'
                    })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Location coordinates or valid location name must be provided'
                })

        point = ee.Geometry.Point(lon, lat)
        buffer = point.buffer(radius * 1000)
        dataset = ee.Image('WorldPop/GP/100m/pop/IND_2020')
        population = dataset.select('population').clip(buffer)
        stats = population.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=buffer,
            scale=90,
            maxPixels=1e9
        )
        population_count = stats.get('population').getInfo()
        population_split = split_population(population_count, urban=is_urban)

        return jsonify({
            'status': 'success',
            'total_population': int(population_count),
            'population_split': population_split
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@validation.route('/location_finder_twitter', methods=['POST'])
def location_finder_twitter():
    try:
        data = request.json
        tweet = data.get('tweet')

        if not tweet:
            return jsonify({
                'status': 'error',
                'message': 'Tweet must be provided'
            })
            
        response = location_model.invoke({
            "tweet": tweet
        })

        return jsonify({
            'status': 'success',
            'locations': response
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })