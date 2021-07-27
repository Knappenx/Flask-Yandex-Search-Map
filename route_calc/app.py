# Flask imports
from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import current_app

# Import Python modules
import urllib
import json
import logging
import math

# Import Keys
import config

# Defining Blueprint
mkad_route = Blueprint(
        "mkad_route",
        __name__,
        static_folder="static",
        template_folder="templates"
    )
# API variable initialization
api_key = config.API_KEY
api_url = (
        "https://geocode-maps.yandex.ru/1.x/?apikey={}" +
        "&format=json&geocode={}&lang=en-US"
    )


def get_distance_from_lat_lon_in_km(lat_1: float, lng_1: float,
                                    lat_2: float, lng_2: float):
    '''
    @function get_distance_from_lat_lon_in_km()
    @brief This function calculates the distance in Kilometers between two
    points on Earth.

    @param lat_1 Latitude from point 1
    @param lng_1 Longitude from point 1
    @param lat_2 Latitude from point 2
    @param lng_2 Longitude from point 2

    @return Distance between point 1 and point 2

    @note function obtained from https://stackoverflow.com/questions/44743075/
            calculate-the-distance-between-two-coordinates-with-python
    '''
    lng_1, lat_1, lng_2, lat_2 = map(
            math.radians, [lng_1, lat_1, lng_2, lat_2]
        )
    d_lat = lat_2 - lat_1
    d_lng = lng_2 - lng_1

    temp = (
         (math.sin(d_lat / 2) ** 2 + math.cos(lat_1)) * (
             math.cos(lat_2) * math.sin(d_lng / 2) ** 2)
    )
    # 6373 is Earth's Radius
    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))


def request_validation(user_address_request: str):
    '''
    @function request_validation()
    @brief This function validates if the address entered by the user is good
            or not.

    @param user_address_request Information obtained from a form POST request

    If not valid:
    @return valid_request False
    @return api_json None

    If valid:
    @return valid_request True
    @return api_json With API response data
    '''
    valid_request = False
    # JSON request and response
    api_response = urllib.request.urlopen(api_url.format(
        api_key, user_address_request)).read()
    api_json = json.loads(api_response)
    found_data = (
            api_json["response"]["GeoObjectCollection"]
            ["metaDataProperty"]["GeocoderResponseMetaData"]["found"]
        )
    # If empty message
    if found_data == "0":
        api_json = None
        return valid_request, api_json
    else:
        valid_request = True
        return valid_request, api_json


def json_clean_data(json_api_data: dict):
    '''
    @function json_clean_data()
    @brief This function extracts required information from a valid Yandex
    GeoCoder API's response.

    @param json_api_data Valid Yandex GeoCoder API's response.

    @return json_dictionary JSON message with data for city and position.
    @return distance_between_points calculated distance between Russian MKAD
            and searched address.
    '''
    MKAD_COORDS = [55.898947, 37.632206]
    position = (json_api_data["response"]["GeoObjectCollection"]
                ["featureMember"][0]["GeoObject"]["Point"]["pos"])
    city = (json_api_data["response"]["GeoObjectCollection"]["featureMember"]
            [0]["GeoObject"]["name"])
    position = position.split(" ")
    latitude = float(position[0])
    longitude = float(position[1])
    # JSON message creation
    json_dictionary = json.dumps([
        {
            "city": city,
            "position": [latitude, longitude]
        }])
    distance_between_points = get_distance_from_lat_lon_in_km(
            longitude,
            latitude,
            MKAD_COORDS[0],
            MKAD_COORDS[1]
        )
    return json_dictionary, distance_between_points


def address_request_from_api():
    '''
    @function address_request_from_api()
    @brief This function extracts required information from a valid Yandex
            GeoCoder API's response.

    @return json_message Cleaned JSON message
    @return address_request Information entered by the user on a POST form
    @return distance Calculated distance between two points on Earth
    @return validation Request validation either True or False
    '''
    # variable initialization
    address_request = None
    distance = None
    json_message = {}
    validation = False
    if request.method == 'POST':
        # Data clean up and verification
        address_request = request.form['address']
        if address_request == "":
            flash(f"Please enter an address or location")
            return json_message, address_request, distance, validation
        else:
            address_request = address_request.replace(" ", "+")
            validation, api_data = request_validation(address_request)
            if validation is False:
                flash(f"No results available")
                return json_message, address_request, distance, validation
            else:
                flash(f"You entered {address_request}", "info")
                json_message, distance = json_clean_data(api_data)
                return json_message, address_request, distance, validation
    return json_message, address_request, distance, validation


def logging_request(request_json: dict, user_post_query: str,
                    distance: float, valid_request: bool):
    '''
    @function logging_request()
    @brief This function writes information in the log file.
            If validation is True, saves JSON message, User's search
            information and the Distance between two points.

    @param request_json Cleaned JSON message.
    @param user_post_query Information entered by the user on a POST form.
    @param distance Calculated distance between two points on Earth.
    @param valid_request Request validation either True or False.
    '''
    logging.basicConfig(
            filename='history.log',
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(threadName)s : %(message)s'
        )
    if valid_request is True:
        current_app.logger.info(f"JSON {request_json}")
        current_app.logger.info(f"Searched for {user_post_query}")
        current_app.logger.info(f"Distance between points is: {distance} Km")
    else:
        current_app.logger.info("Invalid request")


@mkad_route.route("/", methods=['POST', 'GET'])
@mkad_route.route("/home", methods=['POST', 'GET'])
def route_search():
    '''
    @function route_search()
    @brief View which allows users to search for an address or location in
            a map.

    @return Renders the view in a template.
            Passes as context the address or location entered, API KEY and the
            cleaned JSON message.
    '''
    result_json, address, distance, valid_request = address_request_from_api()
    logging_request(result_json, address, distance, valid_request)
    return render_template(
            'search.html',
            address=address,
            api_key=config.API_KEY,
            result_json=result_json
        )
