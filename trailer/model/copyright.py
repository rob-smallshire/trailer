from trailer.model.fieldtools import nullable
from trailer.model.year import Year

class Copyright:

    def __init__(self, author, year=None, license=None):
        self._author = str(author)
        self._year = nullable(Year)(year)
        self._license = nullable(str)(license)


    @property
    def author(self):
        """Copyright holder"""
        return self._author


    @property
    def year(self):
        """Year of copyright."""
        return self._year


    @property
    def license(self):
        """Link to external file containing license text."""
        return self._license