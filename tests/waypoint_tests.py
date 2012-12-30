import unittest
from trailer.model.waypoint import Waypoint

__author__ = 'rjs'

class WaypointTests(unittest.TestCase):

    def test_minimal_create(self):
        wp = Waypoint(45.3524, 90.5652)
        self.assertEqual(wp.latitude, 45.3524)
        self.assertEqual(wp.longitude, 90.5652)
