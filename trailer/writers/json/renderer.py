from collections import OrderedDict
import datetime
import json

__author__ = 'rjs'

class Visitor:
    def visit(self, node, *args, **kwargs):
        method = None
        for cls in node.__class__.__mro__:
            method_name = 'visit_' + cls.__name__
            method = getattr(self, method_name, None)
            if method:
                break

        if not method:
            method = self.generic_visit
        return method(node, *args, **kwargs)


    def generic_visit(self, node, *args, **kwargs):
        raise AttributeError("No visit_" + __class__.__name__ + "method.")


class DecimalSerializableFloat(float):
    """A sublcass of float which can store a decimal.

    This horrible little class is used only to trick the JSON serializer
    to render decimals as numbers without losing precision via float.
    """
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


class GpxJsonEncoder(json.JSONEncoder, Visitor):

    def default(self, obj):
        return self.visit(obj)


    def generic_visit(self, obj, *args, **kwargs):
        return obj


    def optional_attribute_scalar(self, data, obj, name):
        value = getattr(obj, name)
        if value is not None:
            data[name] = self.visit(value)


    def optional_attribute_list(self, data, obj, name):
        values = getattr(obj, name)
        if values:
            data[name] = [ self.visit(item) for item in values ]


    def visit_GpxModel(self, gpx_model, *args, **kwargs):
        """Render a GPXModel as a single JSON structure."""
        result = OrderedDict()

        put_scalar = lambda name: self.optional_attribute_scalar(result, gpx_model, name)
        put_list = lambda name: self.optional_attribute_list(result, gpx_model, name)

        put_scalar('creator')
        put_scalar('metadata')
        put_list('waypoints')
        put_list('routes')
        put_list('tracks')
        put_list('extensions')

        return result


    def visit_Metadata(self, metadata, *args, **kwargs):
        """Render GPX Metadata as a single JSON structure."""
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, metadata, name)
        put_list = lambda name: self.optional_attribute_list(result, metadata, name)

        put_scalar('name')
        put_scalar('description')
        put_scalar('author')
        put_scalar('copyright')
        put_list('links')
        put_scalar('time')
        put_scalar('keywords')
        put_scalar('bounds')
        put_list('extensions')

        return result


    def visit_Person(self, person, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, person, name)

        put_scalar('name')
        put_scalar('email')
        put_scalar('link')

        return result


    def visit_Copyright(self, copyright, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, copyright, name)

        put_scalar('author')
        put_scalar('year')
        put_scalar('license')

        return result


    def visit_Year(self, year, *args, **kwargs):
        dt = datetime.datetime(year=year.year, month=1, day=1, tzinfo=year.tzinfo)
        result = dt.strftime("%Y%z")
        return result


    def visit_Link(self, link, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, link, name)

        put_scalar('href')
        put_scalar('text')
        put_scalar('mime')

        return result


    def visit_datetime(self, dt, *args, **kwargs):
        return dt.isoformat()


    def visit_Bounds(self, bounds, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, bounds, name)

        put_scalar('minimum_latitude')
        put_scalar('minimum_longitude')
        put_scalar('maximum_latitude')
        put_scalar('maximum_longitude')

        return result


    def visit_Decimal(self, d, *args, **kwargs):
        return DecimalSerializableFloat(d)


    def visit_Waypoint(self, waypoint, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, waypoint, name)
        put_list = lambda name: self.optional_attribute_list(result, waypoint, name)

        put_scalar('latitude')
        put_scalar('longitude')
        put_scalar('elevation')
        put_scalar('time')
        put_scalar('magvar')
        put_scalar('geoid_height')
        put_scalar('name')
        put_scalar('comment')
        put_scalar('description')
        put_scalar('source')
        put_list('links')
        put_scalar('symbol')
        put_scalar('classification')
        put_scalar('fix')
        put_scalar('num_satellites')
        put_scalar('hdop')
        put_scalar('vdop')
        put_scalar('pdop')
        put_scalar('seconds_since_dgps_update')
        put_scalar('speed')
        put_scalar('course')
        put_list('extensions')

        return result


    def visit_Route(self, route, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, route, name)
        put_list = lambda name: self.optional_attribute_list(result, route, name)

        put_scalar('name')
        put_scalar('comment')
        put_scalar('description')
        put_scalar('source')
        put_list('links')
        put_scalar('number')
        put_scalar('classification')
        put_list('extensions')
        put_list('points')

        return result


    def visit_Track(self, track, *args, **kwargs):
        result = OrderedDict()
        put_scalar = lambda name: self.optional_attribute_scalar(result, track, name)
        put_list = lambda name: self.optional_attribute_list(result, track, name)

        put_scalar('name')
        put_scalar('comment')
        put_scalar('description')
        put_scalar('source')
        put_list('links')
        put_scalar('number')
        put_scalar('classification')
        put_list('extensions')
        put_list('segments')

        return result

    def visit_Segment(self, segment, *args, **kwargs):
        result = OrderedDict()
        put_list = lambda name: self.optional_attribute_list(result, segment, name)

        put_list('points')
        put_list('extensions')

        return result

    def visit_Fix(self, fix):
        return str(fix)

def main():
    from trailer.readers.parser import parse_gpx
    with open('/Users/rjs/dev/trailer/data/culra.gpx', 'rb') as xml:
        gpx_model = parse_gpx(xml)
        json_data = json.dumps(gpx_model, cls=GpxJsonEncoder)
        return json_data


if __name__ == '__main__':
    gpx_model = main()
    pass