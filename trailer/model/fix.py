__author__ = 'rjs'

class Fix:

    PERMITTED = frozenset(('2d', '3d', 'dgps', 'pps'))

    def __init__(self, value):
        if isinstance(value, Fix):
            value = value._value
        if value not in Fix.PERMITTED:
            raise ValueError("Fix value {0} not permitted".format(value))
        self._value = value

    def __str__(self):
        return self._value

    def __repr__(self):
        return "<Fix(value={0})>".format(repr(self._value))

    def __eq__(self, rhs):
        if isinstance(rhs, Fix):
            return self._value == rhs._value
        return False

    def __ne__(self, rhs):
        return not (self == rhs)