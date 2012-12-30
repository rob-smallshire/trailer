from lxml import etree

from trailer.readers.common import optional_text

from trailer.model.bounds import Bounds
from trailer.model.fieldtools import nullable
from trailer.model.gpx_model import GpxModel
from trailer.model.link import Link
from trailer.model.metadata import Metadata
from trailer.model.person import Person
from trailer.model.route import Route
from trailer.model.segment import Segment
from trailer.model.track import Track
from trailer.model.waypoint import Waypoint

GPX = '{http://www.topografix.com/GPX/1/0}'

def make_links(url, urlname):
    return [Link(url, urlname)] if url is not None or urlname is not None else []


def parse_gpx(xml):
    tree = etree.parse(xml)
    gpx_element = tree.getroot()
    if gpx_element.tag != GPX+'gpx':
        raise ValueError("No gpx root element")

    get_text = lambda tag: optional_text(gpx_element, GPX+tag)

    version = gpx_element.attrib['version']

    if not version.startswith('1.0'):
        raise ValueError("Not a GPX 1.0 file")

    creator = gpx_element.attrib['creator']

    name = get_text('name')
    description = get_text('desc')

    author_name = get_text('author')
    email = get_text('email')
    author = Person(author_name, email)

    url = get_text('url')
    urlname = get_text('urlname')
    links = make_links(url, urlname)

    time = get_text('time')
    keywords = get_text('keywords')

    bounds_element = gpx_element.find(GPX+'bounds')
    bounds = nullable(parse_bounds)(bounds_element)

    metadata = Metadata(name=name, description=description, author=author,
               links=links, time=time, keywords=keywords, bounds=bounds)

    waypoint_elements = gpx_element.findall(GPX+'wpt')
    waypoints = [parse_waypoint(waypoint_element) for waypoint_element in waypoint_elements]

    route_elements = gpx_element.findall(GPX+'rte')
    routes = [parse_route(route_element) for route_element in route_elements]

    track_elements = gpx_element.findall(GPX+'trk')
    tracks = [parse_track(track_element) for track_element in track_elements]

    # TODO : Private elements

    gpx_model  = GpxModel(creator, metadata, waypoints, routes, tracks)

    return gpx_model

def parse_bounds(bounds_element):
    minlat = bounds_element.attrib['minlat']
    minlon = bounds_element.attrib['minlon']
    maxlat = bounds_element.attrib['maxlat']
    maxlon = bounds_element.attrib['maxlon']
    bounds = Bounds(minlat, minlon, maxlat, maxlon)
    return bounds

def parse_waypoint(waypoint_element):
    get_text = lambda tag: optional_text(waypoint_element, GPX+tag)

    latitude = waypoint_element.attrib['lat']
    longitude = waypoint_element.attrib['lon']

    elevation = get_text('ele')
    course = get_text('course')
    speed = get_text('speed')
    time = get_text('time')
    magvar = get_text('magvar')
    geoid_height = get_text('geoidheight')
    name = get_text('name')
    comment = get_text('cmt')
    description = get_text('desc')
    source = get_text('src')

    url = get_text('url')
    urlname = get_text('urlname')
    links = make_links(url, urlname)

    symbol = get_text('sym')
    classification = get_text('type')
    fix = get_text('fix')
    num_satellites = get_text('sat')
    hdop = get_text('hdop')
    vdop = get_text('vdop')
    pdop = get_text('pdop')
    seconds_since_dgps_update = get_text('ageofdgpsdata')
    dgps_station_type = get_text('dgpsid')

    # TODO: Private elements - consider passing private element parser in
    #       to cope with differences between waypoints, routes, etc.

    waypoint = Waypoint(latitude, longitude, elevation, time, magvar,
        geoid_height, name, comment, description, source,
        links, symbol, classification, fix, num_satellites,
        hdop, vdop, pdop, seconds_since_dgps_update,
        dgps_station_type, course, speed)

    return waypoint

def parse_route(route_element):
    get_text = lambda tag: optional_text(route_element, GPX+tag)

    name = get_text('name')
    comment = get_text('cmt')
    description = get_text('desc')
    source = get_text('src')

    url = get_text('url')
    urlname = get_text('urlname')
    links = make_links(url, urlname)

    number = get_text('number')

    routepoint_elements = route_element.findall(GPX+'rtept')
    routepoints = [parse_waypoint(routepoint_element) for routepoint_element in routepoint_elements]

    route = Route(name=name, comment=comment, description=description,
                  source=source, links=links, number=number, points=routepoints)

    return route

def parse_track(track_element):
    get_text = lambda tag: optional_text(track_element, GPX+tag)

    name = get_text('name')
    comment = get_text('comment')
    description = get_text('desc')
    source = get_text('src')

    url = get_text('url')
    urlname = get_text('urlname')
    links = make_links(url, urlname)

    number = get_text('number')

    # TODO: Private elements

    segment_elements = track_element.findall(GPX+'trkseg')
    segments = [parse_segment(segment_element) for segment_element in segment_elements]

    track = Track(name=name, comment=comment, description=description,
                  source=source, links=links, number=number, segments=segments)
    return track


def parse_segment(segment_element):
    trackpoint_elements = segment_element.findall(GPX+'trkpt')
    trackpoints = [parse_waypoint(trackpoint_element) for trackpoint_element in trackpoint_elements]

    segment = Segment(trackpoints)
    return segment


def main():
    with open('/Users/rjs/dev/trailer/data/blue_hills.gpx', 'rb') as xml:
        gpx_model = parse_gpx(xml)
        return gpx_model


if __name__ == '__main__':
    gpx_model = main()
    pass
