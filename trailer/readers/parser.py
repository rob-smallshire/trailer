from lxml import etree
from trailer.readers.common import determine_gpx_namespace

from trailer.readers.gpx_1_0.parser import parse_gpx as parse_gpx_1_0
from trailer.readers.gpx_1_1.parser import parse_gpx as parse_gpx_1_1

def read_gpx(xml, gpxns=None):
    """Parse a GPX file into a GpxModel.

    Args:
        xml: A file-like-object opened in binary mode - that is containing
             bytes rather than characters. The root element of the XML should
             be a <gpx> element containing a version attribute. GPX versions
             1.0 and 1.1 are supported.

        gpxns: The XML namespace for GPX in Clarke notation (i.e. delimited
             by curly braces). If None, (the default) the namespace used in
             the document will be determined automatically.

    Returns:
        A GpxModel representing the data from the supplies xml.

    Raises:
        ValueError: The supplied XML could not be parsed as GPX.
    """
    tree = etree.parse(xml)
    gpx_element = tree.getroot()
    return parse_gpx(gpx_element, gpxns)

def parse_gpx(gpx_element, gpxns=None):
    """Parse a GPX file into a GpxModel.

    Args:
        gpx_element: The root <gpx> element of an XML document containing a
            version attribute. GPX versions 1.0 and 1.1 are supported.

        gpxns: The XML namespace for GPX in Clarke notation (i.e. delimited
             by curly braces).

    Returns:
        A GpxModel representing the data from the supplies xml.

    Raises:
        ValueError: The supplied XML could not be parsed as GPX.
    """
    gpxns = gpxns if gpxns is not None else determine_gpx_namespace(gpx_element)

    if gpx_element.tag != gpxns+'gpx':
        raise ValueError("No gpx root element")

    version = gpx_element.attrib['version']

    if version == '1.0':
        return parse_gpx_1_0(gpx_element, gpxns=gpxns)
    elif version == '1.1':
        return parse_gpx_1_1(gpx_element, gpxns=gpxns)
    else:
        raise ValueError("Cannot parse GPX version {0}".format(version))


def main():
    with open('/Users/rjs/dev/opentrails/data/New_Track_201211261955574100/track.gps', 'rb') as xml:
        gpx_model = read_gpx(xml)
        return gpx_model


if __name__ == '__main__':
    gpx_model = main()
    pass
