import unittest
from trailer.model.gpx_model import GpxModel
from trailer.model.waypoint import Waypoint

__author__ = 'rjs'

class GpxModelTests(unittest.TestCase):

    def test_create_default(self):
        gpx = GpxModel("unittests")
        self.assertEqual(gpx.creator, "unittests")
        self.assertIsNone(gpx.metadata)
        self.assertEqual(len(gpx.waypoints), 0)
        self.assertEqual(len(gpx.routes), 0)
        self.assertEqual(len(gpx.tracks), 0)
        self.assertEqual(len(gpx.extensions), 0)

    def test_create_with_waypoints(self):
        gpx = GpxModel("unittests", waypoints=[Waypoint('23.45', '45.78'),
                                               Waypoint('26.23', '46.23'),
                                               Waypoint('27.12', '44.12')])
        pass

