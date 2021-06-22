from geopy import distance

from core.settings import GEOCODER_KEY

import requests
import polyline
import folium


GEOCODER_ROOT_URL = 'https://maps.googleapis.com/maps/api'


def get_coords(address):
    params = {
        'address': address,
        'key': GEOCODER_KEY
    }

    response = requests.get(
        f'{GEOCODER_ROOT_URL}/geocode/json', params=params).json()

    coords = response['results'][0]['geometry']['location']

    return (coords['lat'], coords['lng'])


def get_route(current_location, buyer_location):
    params = {
        'origin': current_location,
        'destination': buyer_location,
        'key': GEOCODER_KEY,
        'units': 'metric'
    }

    response = requests.get(
        f'{GEOCODER_ROOT_URL}/directions/json', params=params).json()

    steps = response['routes'][0]['legs'][0]['steps']

    points = []

    points = [polyline.decode(step['polyline']['points']) for step in steps]

    return points


def get_distance(vendor_city, buyer_city):
    vendor_coords = get_coords(vendor_city)
    buyer_coords = get_coords(buyer_city)

    return round(distance.distance(vendor_coords, buyer_coords).km, 2)


def get_center_coords(vendor_city, buyer_city):
    buyer_coords = get_coords(buyer_city)
    vendor_coords = get_coords(vendor_city)

    return [(buyer_coords[0] + vendor_coords[0])/2,
            (buyer_coords[1] + vendor_coords[1])/2]


def get_map_zoom(distance):
    if distance <= 3:
        return 15
    elif distance <= 100 and distance > 3:
        return 12
    elif distance > 100 and distance <= 5000:
        return 5
    else:
        return 3


def create_map(buyer_location, current_location, color='orange', icon='stop'):
    buyer_coords = get_coords(buyer_location)
    current_coords = get_coords(current_location)

    distance = get_distance(current_location, buyer_location)

    # to create the map
    m = folium.Map(width=350, height=400,
                   location=get_center_coords(current_location, buyer_location), zoom_start=get_map_zoom(distance))

    # marker for buyer
    folium.Marker(buyer_coords,
                  tooltip='click here for more', popup=buyer_location, icon=folium.Icon(color='red', icon='home')).add_to(m)

    # marker for current location
    folium.Marker(current_coords, tooltip='click here for more',
                  popup=current_location, icon=folium.Icon(color=color, icon=icon)).add_to(m)

    route_points = get_route(current_location, buyer_location)
    # print(route_points)
    # for route between the buyer and the vendor
    line = folium.vector_layers.PolyLine(
        route_points, weigth=2, color='blue')
    m.add_child(line)

    m = m._repr_html_()

    return m


def create_runner_map(location):
    coords = get_coords(location)

    # to create the map
    m = folium.Map(width=350, height=400,
                   location=coords, zoom_start=10)

    # marker for current location
    folium.Marker(coords, tooltip='click here for more',
                  popup=location, icon=folium.Icon(color='red', icon='stop')).add_to(m)

    m = m._repr_html_()

    return m
