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
from trailer.readers.common import optional_text, determine_gpx_namespace


def read_gpx(xml, gpxns=None):
    """Parse a GPX file into a GpxModel.

    Args:
        xml: A file-like-object opened in binary mode - that is containing
             bytes rather than characters. The root element of the XML should
             be a <gpx> element containing a version attribute. GPX version
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

        gpxns: The XML namespace for GPX in Clarke notation (i.e. delimited
             by curly braces). If None, (the default) the namespace used in
             the document will be determined automatically.
    """
    tree = etree.parse(xml)
    gpx_element = tree.getroot()
    return parse_gpx(gpx_element, gpxns=gpxns)

def parse_gpx(gpx_element, gpx_extensions_parser=None,
                   metadata_extensions_parser=None,
                   waypoint_extensions_parser=None,
                   route_extensions_parser=None,
                   track_extensions_parser=None,
                   segment_extensions_parser=None,
                   gpxns=None):
    """Parse a GPX file into a GpxModel.

    Args:
        gpx_element: gpx_element: The root <gpx> element of an XML document
            containing a version attribute. GPX versions 1.1 is supported.

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
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(gpx_element)

    if gpx_element.tag != gpxns+'gpx':
        raise ValueError("No gpx root element")

    creator = gpx_element.attrib['creator']
    version = gpx_element.attrib['version']

    if not version.startswith('1.1'):
        raise ValueError("Not a GPX 1.1 file")

    metadata_element = gpx_element.find(gpxns+'metadata')
    metadata = nullable(parse_metadata)(metadata_element, gpxns)

    waypoint_elements = gpx_element.findall(gpxns+'wpt')
    waypoints = [parse_waypoint(waypoint_element, gpxns) for waypoint_element in waypoint_elements]

    route_elements = gpx_element.findall(gpxns+'rte')
    routes = [parse_route(route_element, gpxns) for route_element in route_elements]

    track_elements = gpx_element.findall(gpxns+'trk')
    tracks = [parse_track(track_element, gpxns) for track_element in track_elements]

    extensions_element = gpx_element.find(gpxns+'extensions')
    extensions = nullable(parse_gpx_extensions)(extensions_element, gpxns)

    gpx_model = GpxModel(creator, metadata, waypoints, routes, tracks,
                         extensions)

    return gpx_model


def parse_metadata(metadata_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(metadata_element)

    get_text = lambda tag: optional_text(metadata_element, gpxns+tag)

    name = get_text('name')
    description = get_text('desc')

    author_element = metadata_element.find(gpxns+'author')
    author = nullable(parse_person)(author_element, gpxns)

    copyright_element = metadata_element.find(gpxns+'copyright')
    copyright = nullable(parse_copyright)(copyright_element, gpxns)

    link_elements = metadata_element.findall(gpxns+'link')
    links = [parse_link(link_element, gpxns) for link_element in link_elements]

    time = get_text('time')
    keywords = get_text('keywords')

    bounds_element = metadata_element.find(gpxns+'bounds')
    bounds = nullable(parse_bounds)(bounds_element)

    extensions_element = metadata_element.find(gpxns+'extensions')
    extensions = nullable(parse_metadata_extensions)(extensions_element, gpxns)

    return Metadata(name, description, author, copyright, links, time,
                    keywords, bounds, extensions)


def parse_person(person_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(person_element)

    get_text = lambda tag: optional_text(person_element, gpxns+tag)

    name = get_text('name')

    email_element = person_element.find(gpxns+'email')
    email = nullable(parse_email)(email_element, gpxns)

    link_element = person_element.find(gpxns+'link')
    link = nullable(parse_link)(link_element, gpxns)

    return Person(name, email, link)


def parse_email(email_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(email_element)

    get_text = lambda tag: optional_text(email_element, gpxns+tag)

    id = get_text('id')
    domain = get_text('domain')
    return id +  '@' + domain


def parse_copyright(copyright_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(copyright_element)

    get_text = lambda tag: optional_text(copyright_element, gpxns+tag)

    author = copyright_element.attrib['author']

    year_element = copyright_element.find(gpxns+'year')
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


def parse_waypoint(waypoint_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(waypoint_element)

    get_text = lambda tag: optional_text(waypoint_element, gpxns+tag)

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

    link_elements = waypoint_element.findall(gpxns+'link')
    links = [parse_link(link_element, gpxns) for link_element in link_elements]

    symbol = get_text('sym')
    classification = get_text('type')
    fix = get_text('fix')
    num_satellites = get_text('sat')
    hdop = get_text('hdop')
    vdop = get_text('vdop')
    pdop = get_text('pdop')
    seconds_since_dgps_update = get_text('ageofdgpsdata')
    dgps_station_type = get_text('dgpsid')

    extensions_element = waypoint_element.find(gpxns+'extensions')
    extensions = nullable(parse_waypoint_extensions)(extensions_element, gpxns)

    waypoint = Waypoint(latitude, longitude, elevation, time, magvar,
                        geoid_height, name, comment, description, source,
                        links, symbol, classification, fix, num_satellites,
                        hdop, vdop, pdop, seconds_since_dgps_update,
                        dgps_station_type, extensions)
    return waypoint


def parse_link(link_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(link_element)

    get_text = lambda tag: optional_text(link_element, gpxns+tag)

    href = link_element.attrib['href']
    text = get_text('text')
    mime = get_text('type')

    link = Link(href, text, mime)
    return link


def parse_route(route_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(route_element)

    get_text = lambda tag: optional_text(route_element, gpxns+tag)

    name = get_text('name')
    comment = get_text('cmt')
    description = get_text('desc')
    source = get_text('src')

    link_elements = route_element.findall(gpxns+'link')
    links = [parse_link(link_element, gpxns) for link_element in link_elements]

    number = get_text('number')
    classification = get_text('type')

    extensions_element = route_element.find(gpxns+'extensions')
    extensions = nullable(parse_route_extensions)(extensions_element, gpxns)

    routepoint_elements = route_element.findall(gpxns+'rtept')
    routepoints = [parse_waypoint(routepoint_element, gpxns) for routepoint_element in routepoint_elements]

    route = Route(name, comment, description, source, links, number, classification, extensions, routepoints)

    return route


def parse_track(track_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(track_element)

    get_text = lambda tag: optional_text(track_element, gpxns+tag)

    name = get_text('name')
    comment = get_text('comment')
    description = get_text('desc')
    source = get_text('src')

    link_elements = track_element.findall(gpxns+'link')
    links = [parse_link(link_element, gpxns) for link_element in link_elements]

    number = get_text('number')
    classification = get_text('type')

    segment_elements = track_element.findall(gpxns+'trkseg')
    segments = [parse_segment(segment_element, gpxns) for segment_element in segment_elements]

    extensions_element = track_element.find(gpxns+'extensions')
    extensions = nullable(parse_track_extensions)(extensions_element, gpxns)

    track = Track(name, comment, description, source, links, number,
                  classification, extensions, segments)
    return track


def parse_segment(segment_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(segment_element)

    trackpoint_elements = segment_element.findall(gpxns+'trkpt')
    trackpoints = [parse_waypoint(trackpoint_element, gpxns) for trackpoint_element in trackpoint_elements]

    extensions_element = segment_element.find(gpxns+'extensions')
    extensions = nullable(parse_segment_extensions)(extensions_element, gpxns)

    segment = Segment(trackpoints, extensions)
    return segment


def parse_gpx_extensions(extensions_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(extensions_element)
    return None


def parse_metadata_extensions(extensions_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(extensions_element)
    return None


def parse_waypoint_extensions(extensions_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(extensions_element)
    return None


def parse_route_extensions(extensions_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(extensions_element)
    return None


def parse_track_extensions(extensions_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(extensions_element)
    return None


def parse_segment_extensions(extensions_element, gpxns=None):
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(extensions_element)
    return None


def main():
    with open('/Users/rjs/dev/trailer/data/Wypt 001.gpx', 'rb') as xml:
        gpx_model = read_gpx(xml)
        return gpx_model


if __name__ == '__main__':
    gpx_model = main()
    pass
