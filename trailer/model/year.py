

class Year:

    def __init__(self, year, tzinfo=None):
        if tzinfo is None:
            if isinstance(year, Year):
                self._year = year.year
                self._tzinfo = year.tzinfo
            else:
                self._year = int(year)
                self._tzinfo = None
        else:
            self._year = int(year)
            self._tzinfo = tzinfo

    @property
    def year(self):
        return self._year

    @property
    def tzinfo(self):
        return self._tzinfo