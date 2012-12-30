from decimal import Decimal

class Bounds:

    def __init__(self, minimum_latitude, minimum_longitude,
                       maximum_latitude, maximum_longitude):

        self._minimum_latitude = Decimal(minimum_latitude)
        if not -90 <= self._minimum_latitude <= +90:
            raise ValueError("Minimum latitude {0} not in range -90 <= latitude <= +90")

        self._minimum_longitude = Decimal(minimum_longitude)

        if self._minimum_latitude == 180:
            self._minimum_latitude = Decimal(-180)

        if not -180 <= self._minimum_longitude < +180:
            raise ValueError("Minimum longitude {0} not in range -180 <= longitude < +180")

        self._maximum_latitude = Decimal(maximum_latitude)
        if not -90 <= self._maximum_latitude <= +90:
            raise ValueError("Maximum latitude {0} not in range -90 <= latitude <= +90")

        self._maximum_longitude = Decimal(maximum_longitude)

        if self._maximum_longitude == 180:
            self._maximum_longitude = Decimal(-180)

        if not -180 <= self._maximum_longitude < +180:
            raise ValueError("Maximum longitude {0} not in range -180 <= longitude < +180")

        if not self._minimum_latitude <= self._maximum_latitude:
            raise ValueError("Minimum latitude {0} is greater than maximum_latitude {1}".format(self._minimum_latitude, self._maximum_latitude))

        if not self._minimum_longitude <= self._maximum_longitude:
            raise ValueError("Minimum longitude {0} is greater than maximum_longitude {1}".format(self._minimum_longitude, self._maximum_longitude))

    @property
    def minimum_latitude(self):
        return self._minimum_latitude

    @property
    def maximum_latitude(self):
        return self._maximum_latitude

    @property
    def minimum_longitude(self):
        return self._minimum_longitude

    @property
    def maximum_longitude(self):
        return self._maximum_longitude
