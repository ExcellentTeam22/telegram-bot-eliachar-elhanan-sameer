class Location:
    def __init__(self, street, city, country, region='IL') -> None:
        self.street = street
        self.city = city
        self.country = country
        self.region = region
        self.found_coords = False

    def add_coords(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.found_coords = True

    def __str__(self):
        return self.street + ' ' + self.city + ' ' + self.country + ' ' + self.region if not self.found_coords else \
            self.street + ' ' + self.city + ' ' + self.country + ' ' + self.region + \
            ': (' + str(self.lat) + ', ' + str(self.lon) + ')'


