from enum import Enum


class RadiusUnit(Enum):
    KILOMETER = "km"
    MILES = "mi"


class GeoCode:
    def __init__(self, lat, lng, radius, radius_unit: RadiusUnit):
        self.lat = lat
        self.lng = lng
        self.radius = radius
        self.radius_unit = radius_unit

    def to_tweepy_str(self):
        return f"{self.lat},{self.lng},{self.radius}{self.radius_unit}"
