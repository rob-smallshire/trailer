

from trailer.model.fieldtools import nullable, make_list, make_time

class Metadata:
    """
    Information about the GPX file, author, and copyright restrictions goes in
    the metadata section. Providing rich, meaningful information about your
    GPX files allows others to search for and use your GPS data.
    """


    def __init__(self, name=None, description=None, author=None,
                 copyright=None, links=None, time=None, keywords=None,
                 bounds=None, extensions=None):
        self._name = nullable(str)(name)
        self._description = nullable(str)(description)
        self._author = author
        self._copyright = copyright
        self._links = make_list(links)
        self._time = nullable(make_time)(time)
        self._keywords = nullable(str)(keywords)
        self._bounds = bounds
        self._extensions = make_list(extensions)

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def author(self):
        return self._author

    @property
    def copyright(self):
        return self._copyright

    @property
    def links(self):
        return self._links

    @property
    def time(self):
        return self._time

    @property
    def keywords(self):
        return self._keywords

    @property
    def bounds(self):
        return self._bounds

    @property
    def extensions(self):
        return self._extensions



