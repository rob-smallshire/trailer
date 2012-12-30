from trailer.model.fieldtools import make_list

__author__ = 'rjs'

class Segment:
    """An ordered list of track points.

    A Track Segment holds a list of Track Points which are logically
    connected in order. To represent a single GPS track where GPS reception
    was lost, or the GPS receiver was turned off, start a new Track Segment
    for each continuous span of track data.
    """
    def __init__(self, points=None, extensions=None):
        self._points = make_list(points)
        self._extensions = make_list(extensions)

    @property
    def points(self):
        return self._points

    @property
    def extensions(self):
        return self._extensions

