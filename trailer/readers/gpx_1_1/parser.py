import re

import dateutil.parser

from lxml import etree

from trailer.model.bounds import Bounds
from trailer.model.copyright import Copyright
from trailer.model.fieldtools import nullable
from trailer.model.gpx_model import GpxModel
from trailer.model.link import Link
from trailer.model.metadata import Metadata
from trailer.model.person import Person
from trailer.model.route import Route
from trailer.model.segment import Segment
from trailer.model.track import Track
from trailer.model.waypoint import Waypoint
from trailer.model.year import Year
from trailer.readers.common import optional_text

GPX = '{http://www.topografix.com/GPX/1/1}'

def parse_gpx(xml, gpx_extensions_parser=None,
                   metadata_extensions_parser=None,
                   waypoint_extensions_parser=None,
                   route_extensions_parser=None,
                   track_extensions_parser=None,
                   segment_extensions_parser=None):
    """Parse a GPX file into a GpxModel.

    Args:
        xml: A file-like-object opened in binary mode - that is containing
             bytes rather than characters. The root element of the XML should
             be a <gpx> element containing a version attribute. GPX versions
             1.1 is supported.

        gpx_extensions_parser: An optional callable which accepts an Element
            with the 'extensions' tag and returns a list of model objects
            representing the extensions. If not specified, extensions are
            ignored.

        metadata_extensions_parser: An optional callable which accepts an
            Element with the 'extensions' tag and returns a list of model
            objects representing the extensions. If not specified, extensions
            are ignored.

        waypoint_extensions_parser: An optional callable which accepts an
            Element with the 'extensions' tag and returns a list of model
            objects representing the extensions. If not specified, extensions
            are ignored.

        route_extensions_parser: An optional callable which accepts an Element
            with the 'extensions' tag and returns a list of model objects
            representing the extensions. If not specified, extensions are
            ignored.

        track_extensions_parser: An optional callable which accepts an Element
            with the 'extensions' tag and returns a list of model objects
            representing the extensions. If not specified, extensions are
            ignored.

        segment_extensions_parser: An optional callable which accepts an
            Element with the 'extensions' tag and returns a list of model
            objects representing the extensions. If not specified, extensions
            are ignored.


    Returns:
        A GpxModel representing the data from the supplies xml.

    Raises:
        ValueError: The supplied XML could not be parsed as GPX.
    """
    tree = etree.parse(xml)
    gpx_element = tree.getroot()
    if gpx_element.tag != GPX+'gpx':
        raise ValueError("No gpx root element")

    creator = gpx_element.attrib['creator']
    version = gpx_element.attrib['version']

    if not version.startswith('1.1'):
        raise ValueError("Not a GPX 1.1 file")

    metadata_element = gpx_element.find(GPX+'metadata')
    metadata = nullable(parse_metadata)(metadata_element)

    waypoint_elements = gpx_element.findall(GPX+'wpt')
    waypoints = [parse_waypoint(waypoint_element) for waypoint_element in waypoint_elements]

    route_elements = gpx_element.findall(GPX+'rte')
    routes = [parse_route(route_element) for route_element in route_elements]

    track_elements = gpx_element.findall(GPX+'trk')
    tracks = [parse_track(track_element) for track_element in track_elements]

    extensions_element = metadata_element.find(GPX+'extensions')
    extensions = nullable(parse_gpx_extensions)(extensions_element)

    gpx_model = GpxModel(creator, metadata, waypoints, routes, tracks,
                         extensions)

    return gpx_model


def parse_metadata(metadata_element):
    get_text = lambda tag: optional_text(metadata_element, GPX+tag)

    name = get_text('name')
    description = get_text('desc')

    author_element = metadata_element.find(GPX+'author')
    author = nullable(parse_person)(author_element)

    copyright_element = metadata_element.find(GPX+'copyright')
    copyright = nullable(parse_copyright)(copyright_element)

    link_elements = metadata_element.findall(GPX+'link')
    links = [parse_link(link_element) for link_element in link_elements]

    time = get_text('time')
    keywords = get_text('keywords')

    bounds_element = metadata_element.find(GPX+'bounds')
    bounds = nullable(parse_bounds)(bounds_element)

    extensions_element = metadata_element.find(GPX+'extensions')
    extensions = nullable(parse_metadata_extensions)(extensions_element)

    return Metadata(name, description, author, copyright, links, time,
                    keywords, bounds, extensions)


def parse_person(person_element):
    get_text = lambda tag: optional_text(person_element, GPX+tag)

    name = get_text('name')

    email_element = person_element.find(GPX+'email')
    email = nullable(parse_email)(email_element)

    link_element = person_element.find(GPX+'link')
    link = nullable(parse_link)(link_element)

    return Person(name, email, link)


def parse_email(email_element):
    get_text = lambda tag: optional_text(email_element, GPX+tag)

    id = get_text('id')
    domain = get_text('domain')
    return id +  '@' + domain


def parse_copyright(copyright_element):
    get_text = lambda tag: optional_text(copyright_element, GPX+tag)

    author = copyright_element.attrib['author']

    year_element = copyright_element.find(GPX+'year')
    year = nullable(parse_year)(year_element)

    license = get_text('license')

    return Copyright(author, year, license)


MIDNIGHT_JAN_1 = '-Jan-01t00:00'

GYEAR_REGEX = re.compile(r'(\d{4,})(.*)')

def parse_year(year_element):
    text = year_element.text
    match = GYEAR_REGEX.match(text)
    if not match:
        raise ValueError('Invalid xsd:gYear value "{0}"'.format(text))
    year = match.group(1)
    timezone = match.group(2)
    year_start = year + MIDNIGHT_JAN_1 + timezone
    dt = dateutil.parser.parse(year_start)
    return Year(dt.year, dt.tzinfo)


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
    time = get_text('time')
    magvar = get_text('magvar')
    geoid_height = get_text('geoidheight')
    name = get_text('name')
    comment = get_text('cmt')
    description = get_text('desc')
    source = get_text('src')

    link_elements = waypoint_element.findall(GPX+'link')
    links = [parse_link(link_element) for link_element in link_elements]

    symbol = get_text('sym')
    classification = get_text('type')
    fix = get_text('fix')
    num_satellites = get_text('sat')
    hdop = get_text('hdop')
    vdop = get_text('vdop')
    pdop = get_text('pdop')
    seconds_since_dgps_update = get_text('ageofdgpsdata')
    dgps_station_type = get_text('dgpsid')

    extensions_element = waypoint_element.find(GPX+'extensions')
    extensions = nullable(parse_waypoint_extensions)(extensions_element)

    waypoint = Waypoint(latitude, longitude, elevation, time, magvar,
                        geoid_height, name, comment, description, source,
                        links, symbol, classification, fix, num_satellites,
                        hdop, vdop, pdop, seconds_since_dgps_update,
                        dgps_station_type, extensions)
    return waypoint


def parse_link(link_element):
    get_text = lambda tag: optional_text(link_element, GPX+tag)

    href = link_element.attrib['href']
    text = get_text('text')
    mime = get_text('type')

    link = Link(href, text, mime)
    return link


def parse_route(route_element):
    get_text = lambda tag: optional_text(route_element, GPX+tag)

    name = get_text('name')
    comment = get_text('cmt')
    description = get_text('desc')
    source = get_text('src')

    link_elements = route_element.findall(GPX+'link')
    links = [parse_link(link_element) for link_element in link_elements]

    number = get_text('number')
    classification = get_text('type')

    extensions_element = route_element.find(GPX+'extensions')
    extensions = nullable(parse_route_extensions)(extensions_element)

    routepoint_elements = route_element.findall(GPX+'rtept')
    routepoints = [parse_waypoint(routepoint_element) for routepoint_element in routepoint_elements]

    route = Route(name, comment, description, source, links, number, classification, extensions, routepoints)

    return route


def parse_track(track_element):
    get_text = lambda tag: optional_text(track_element, GPX+tag)

    name = get_text('name')
    comment = get_text('comment')
    description = get_text('desc')
    source = get_text('src')

    link_elements = track_element.findall(GPX+'link')
    links = [parse_link(link_element) for link_element in link_elements]

    number = get_text('number')
    classification = get_text('type')

    segment_elements = track_element.findall(GPX+'trkseg')
    segments = [parse_segment(segment_element) for segment_element in segment_elements]

    extensions_element = track_element.find(GPX+'extensions')
    extensions = nullable(parse_track_extensions)(extensions_element)

    track = Track(name, comment, description, source, links, number,
                  classification, extensions, segments)
    return track


def parse_segment(segment_element):
    trackpoint_elements = segment_element.findall(GPX+'trkpt')
    trackpoints = [parse_waypoint(trackpoint_element) for trackpoint_element in trackpoint_elements]

    extensions_element = segment_element.find(GPX+'extensions')
    extensions = nullable(parse_segment_extensions)(extensions_element)

    segment = Segment(trackpoints, extensions)
    return segment


def parse_gpx_extensions(extensions_elements):
    return None


def parse_metadata_extensions(extensions_element):
    return None


def parse_waypoint_extensions(extensions_element):
    return None


def parse_route_extensions(extensions_element):
    return None


def parse_track_extensions(extensions_element):
    return None


def parse_segment_extensions(extensions_element):
    return None


def main():
    with open('/Users/rjs/dev/trailer/data/Wypt 001.gpx', 'rb') as xml:
        gpx_model = parse_gpx(xml)
        return gpx_model


if __name__ == '__main__':
    gpx_model = main()
    pass
