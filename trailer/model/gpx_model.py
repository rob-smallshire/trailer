from trailer.model.fieldtools import make_list

class GpxModel:

    def __init__(self, creator, metadata=None, waypoints=None, routes=None,
                 tracks=None, extensions=None):
        self._creator = creator
        self._metadata = metadata
        self._waypoints = make_list(waypoints)
        self._routes = make_list(routes)
        self._tracks = make_list(tracks)
        self._extensions = make_list(extensions)

    @property
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, value):
        self._creator = value

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @property
    def waypoints(self):
        return self._waypoints

    @property
    def routes(self):
        return self._routes

    @property
    def tracks(self):
        return self._tracks

    @property
    def extensions(self):
        return self._extensions






