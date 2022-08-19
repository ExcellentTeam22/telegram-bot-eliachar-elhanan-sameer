import logging
import re
import requests

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)


class WRCError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WazeRouteCalculator(object):
    """Calculate actual route time and distance with Waze API"""

    WAZE_URL = "https://www.waze.com/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "referer": WAZE_URL,
    }
    VEHICLE_TYPES = ('TAXI', 'MOTORCYCLE')
    BASE_COORDS = {
        'US': {"lat": 40.713, "lon": -74.006},
        'EU': {"lat": 47.498, "lon": 19.040},
        'IL': {"lat": 31.768, "lon": 35.214},
        'AU': {"lat": -35.281, "lon": 149.128}
    }
    COORD_SERVERS = {
        'US': 'SearchServer/mozi',
        'EU': 'row-SearchServer/mozi',
        'IL': 'il-SearchServer/mozi',
        'AU': 'row-SearchServer/mozi'
    }
    ROUTING_SERVERS = {
        'US': 'RoutingManager/routingRequest',
        'EU': 'row-RoutingManager/routingRequest',
        'IL': 'il-RoutingManager/routingRequest',
        'AU': 'row-RoutingManager/routingRequest'
    }
    COORD_MATCH = re.compile(r'^([-+]?)([\d]{1,2})(((\.)(\d+)(,)))(\s*)(([-+]?)([\d]{1,3})((\.)(\d+))?)$')

    def __init__(self, address, region='IL', vehicle_type='', avoid_toll_roads=False, avoid_subscription_roads=False, avoid_ferries=False, log_lvl=None):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())
        if log_lvl:
            self.log.warning("log_lvl is deprecated please check example.py ")
        self.log.info("From: %s - to: %s", address)
        region = region.upper()
        if region == 'NA':  # North America
            region = 'US'
        self.region = region
        self.vehicle_type = ''
        if vehicle_type and vehicle_type in self.VEHICLE_TYPES:
            self.vehicle_type = vehicle_type.upper()
        self.ROUTE_OPTIONS = {
            'AVOID_TRAILS': 't',
            'AVOID_TOLL_ROADS': 't' if avoid_toll_roads else 'f',
            'AVOID_FERRIES': 't' if avoid_ferries else 'f'
        }
        self.avoid_subscription_roads = avoid_subscription_roads
        if self.already_coords(address):  # See if we have coordinates or address to resolve
            self.start_coords = self.coords_string_parser(address)
        else:
            self.start_coords = self.address_to_coords(address)
        self.log.debug('Start coords: (%s, %s)', self.start_coords["lat"], self.start_coords["lon"])

    def already_coords(self, address):
        """test used to see if we have coordinates or address"""

        m = re.search(self.COORD_MATCH, address)
        return (m is not None)

    def coords_string_parser(self, coords):
        """Pareses the address string into coordinates to match address_to_coords return object"""

        lat, lon = coords.split(',')
        return {"lat": lat.strip(), "lon": lon.strip(), "bounds": {}}

    def address_to_coords(self, address):
        """Convert address to coordinates"""

        base_coords = self.BASE_COORDS[self.region]
        get_cord = self.COORD_SERVERS[self.region]
        url_options = {
            "q": address,
            "lang": "eng",
            "origin": "livemap",
            "lat": base_coords["lat"],
            "lon": base_coords["lon"]
        }

        response = requests.get(self.WAZE_URL + get_cord, params=url_options, headers=self.HEADERS)
        for response_json in response.json():
            if response_json.get('city'):
                lat = response_json['location']['lat']
                lon = response_json['location']['lon']
                bounds = response_json['bounds']  # sometimes the coords don't match up
                if bounds is not None:
                    bounds['top'], bounds['bottom'] = max(bounds['top'], bounds['bottom']), min(bounds['top'], bounds['bottom'])
                    bounds['left'], bounds['right'] = min(bounds['left'], bounds['right']), max(bounds['left'], bounds['right'])
                else:
                    bounds = {}
                return {"lat": lat, "lon": lon}
        raise WRCError("Cannot get coords for %s" % address)

    def get_route(self, npaths=1, time_delta=0):
        """Get route data from waze"""

        routing_server = self.ROUTING_SERVERS[self.region]

        url_options = {
            "from": "x:%s y:%s" % (self.start_coords["lon"], self.start_coords["lat"]),
            "to": "x:%s y:%s" % (self.end_coords["lon"], self.end_coords["lat"]),
            "at": time_delta,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": npaths,
            "options": ','.join('%s:%s' % (opt, value) for (opt, value) in self.ROUTE_OPTIONS.items()),
        }
        if self.vehicle_type:
            url_options["vehicleType"] = self.vehicle_type
        # Handle vignette system in Europe. Defaults to false (show all routes)
        if self.avoid_subscription_roads is False:
            url_options["subscription"] = "*"

        response = requests.get(self.WAZE_URL + routing_server, params=url_options, headers=self.HEADERS)
        response.encoding = 'utf-8'
        response_json = self._check_response(response)
        if response_json:
            if 'error' in response_json:
                raise WRCError(response_json.get("error"))
            else:
                if response_json.get("alternatives"):
                    return [alt['response'] for alt in response_json['alternatives']]
                response_obj = response_json['response']
                if isinstance(response_obj, list):
                    response_obj = response_obj[0]
                if npaths > 1:
                    return [response_obj]
                return response_obj
        else:
            raise WRCError("empty response")