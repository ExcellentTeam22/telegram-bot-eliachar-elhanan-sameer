
import waze_classes as waze
# import WazeRouteCalculator
from location import Location


def get_coords_lon_lat(location: Location):
    route = waze.WazeRouteCalculator(str(location), region=location.region)
    dict_lat_lon = route.address_to_coords(str(location))
    return dict_lat_lon['lat'], dict_lat_lon['lon']


def create_location(street, city, country, region):
    return Location(street=street, city=city, country=country, region=region)


def check(street, city, country, region):
    location = create_location(street, city, country, region)
    print(location)

    lat, lon = get_coords_lon_lat(location)

    location.add_coords(lat, lon)
    print(location)


if __name__ == '__main__':

    check(street='Agripas', city='Jerusalem', country='Israel', region='IL')
    check(street='Ofira', city='Jerusalem', country='Israel', region='IL')
    check(street='Shoham', city='Jerusalem', country='Israel', region='IL')
    check(street='Dizengoff', city='Tel Aviv', country='Israel', region='IL')
    check(street='Dizengoff', city='Tel-Aviv', country='Israel', region='IL')
    check(street='Crimee', city='Paris', country='France', region='EU')


    # get_coords_lon_lat(street='Agripas', city='Jerusalem', country='Israel', region='IL')
    # get_coords_lon_lat(street='Ofira', city='Jerusalem', country='Israel', region='IL')
    # get_coords_lon_lat(street='Shoham', city='Jerusalem', country='Israel', region='IL')
    # get_coords_lon_lat(street='Dizengoff', city='Tel Aviv', country='Israel', region='IL')
    # get_coords_lon_lat(street='Dizengoff', city='Tel-Aviv', country='Israel', region='IL')





    # get_coords_lon_lat('Budapest, Hungary')
    # get_coords_lon_lat('Paris, France')
    # get_coords_lon_lat('Jerusalem, Israel')

    # geolocator = Nominatim(user_agent="specify_your_app_name_here")
    # location = geolocator.geocode("Agripas Jerusalem")
    # print(location.address)
    # print((location.latitude, location.longitude))

    # gn = geocoders.Google()
    # place, (lat, lng) = gn.geocode(city)
    # print(place)
    # print(lat)
    # print(lng)
    # from_address = country + ', ' + city + ', ' + street

    # import logging
    # import requests
    # import re
    # from geopy import geocoders
    # from geopy.geocoders import Nominatim