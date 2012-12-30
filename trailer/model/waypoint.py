from decimal import Decimal
from trailer.model.fix import Fix
from trailer.model.fieldtools import nullable, make_list, make_time

class Waypoint:

    def __init__(self, latitude, longitude, elevation=None, time=None,
                 magvar=None, geoid_height=None, name=None, comment=None,
                 description=None, source=None, links=None, symbol=None,
                 classification=None, fix=None, num_satellites=None,
                 hdop=None, vdop=None, pdop=None,
                 seconds_since_dgps_update=None, dgps_station_type=None,
                 speed=None, course=None,
                 extensions=None):

        self._latitude = Decimal(latitude)
        if not -90 <= self._latitude <= +90:
            raise ValueError("Latitude {0} not in range -90 <= latitude <= +90")

        self._longitude = Decimal(longitude)
        if not -180 <= self._longitude < +180:
            raise ValueError("Longitude {0} not in range -180 <= longitude < +180")

        self._elevation = nullable(Decimal)(elevation)
        self._time = nullable(make_time)(time)

        self._magvar = nullable(Decimal)(magvar)
        if self._magvar is not None:
            if not 0 <= self._magvar < 360:
                raise ValueError("Magnetic variation {0} not in range 0 <= magvar < 360")

        self._geoid_height = nullable(Decimal)(geoid_height)
        self._name = nullable(str)(name)
        self._comment = nullable(str)(comment)
        self._description = nullable(str)(description)
        self._source = nullable(str)(source)
        self._links = make_list(links)
        self._symbol = nullable(str)(symbol)
        self._classification = nullable(str)(classification)
        self._fix = nullable(Fix)(fix)

        self._num_satellites = nullable(int)(num_satellites)
        if self._num_satellites is not None:
            if self._num_satellites < 0:
                raise ValueError("Number of satellites {0} cannot be negative")

        self._hdop = nullable(Decimal)(hdop)
        self._vdop = nullable(Decimal)(vdop)
        self._pdop = nullable(Decimal)(pdop)

        self._seconds_since_dgps_update = nullable(Decimal)(seconds_since_dgps_update)

        self._dgps_station_type = nullable(int)(dgps_station_type)
        if self._dgps_station_type is not None:
            if not 0 <= self._dgps_station_type <= 1023:
                raise ValueError("DGPS station type {0} not in range 0 <= dgps_station_type <= 1023")

        self._speed = nullable(Decimal)(speed)

        self._course = nullable(Decimal)(course)
        if self._course is not None:
            if not 0 <= self._course < 360:
                raise ValueError("Course {0} not in range 0 <= course < 360")

        self._extensions = make_list(extensions)

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def elevation(self):
        return self._elevation

    @property
    def time(self):
        return self._time

    @property
    def magvar(self):
        return self._magvar

    @property
    def geoid_height(self):
        return self._geoid_height

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

    @property
    def description(self):
        return self._description

    @property
    def source(self):
        return self._source

    @property
    def links(self):
        return self._links

    @property
    def symbol(self):
        return self._symbol

    @property
    def classification(self):
        return self._classification

    @property
    def fix(self):
        return self._fix

    @property
    def num_satellites(self):
        return self._num_satellites

    @property
    def hdop(self):
        return self._hdop

    @property
    def vdop(self):
        return self._vdop

    @property
    def pdop(self):
        return self._pdop

    @property
    def seconds_since_dgps_update(self):
        return self._seconds_since_dgps_update

    @property
    def dgps_station_type(self):
        return self._dgps_station_type

    @property
    def speed(self):
        return self._speed

    @property
    def course(self):
        return self._course

    @property
    def extensions(self):
        return self._extensions