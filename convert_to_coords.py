
import waze_classes as waze
# import WazeRouteCalculator


def get_coords_lon_lat(street, city, country, region):
    address = street + ' ' + city + ' ' + country
    route = waze.WazeRouteCalculator(address, region=region)
    dict_lat_lon = route.address_to_coords(address)
    print(dict_lat_lon)


if __name__ == '__main__':
    get_coords_lon_lat(street='Agripas', city='Jerusalem', country='Israel', region='IL')
    get_coords_lon_lat(street='Ofira', city='Jerusalem', country='Israel', region='IL')
    get_coords_lon_lat(street='Shoham', city='Jerusalem', country='Israel', region='IL')
    get_coords_lon_lat(street='Dizengoff', city='Tel Aviv', country='Israel', region='IL')
    get_coords_lon_lat(street='Dizengoff', city='Tel-Aviv', country='Israel', region='IL')





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