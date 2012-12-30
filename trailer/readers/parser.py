from lxml import etree

from trailer.readers.gpx_1_0.parser import parse_gpx as parse_gpx_1_0
from trailer.readers.gpx_1_1.parser import parse_gpx as parse_gpx_1_1

GPX = '{http://www.topografix.com/GPX/1/0}'

def parse_gpx(xml):
    """Parse a GPX file into a GpxModel.

    Args:
        xml: A file-like-object opened in binary mode - that is containing
             bytes rather than characters. The root element of the XML should
             be a <gpx> element containing a version attribute. GPX versions
             1.0 and 1.1 are supported.

    Returns:
        A GpxModel representing the data from the supplies xml.

    Raises:
        ValueError: The supplied XML could not be parsed as GPX.
    """
    tree = etree.parse(xml)
    gpx_element = tree.getroot()
    if gpx_element.tag != GPX+'gpx':
        raise ValueError("No gpx root element")

    version = gpx_element.attrib['version']

    xml.seek(0)

    if version == '1.0':
        return parse_gpx_1_0(xml)
    elif version == '1.1':
        return parse_gpx_1_1(xml)
    else:
        raise ValueError("Cannot parse GPX version {0}".format(version))


def main():
    with open('/Users/rjs/dev/trailer/data/blue_hills.gpx', 'rb') as xml:
        gpx_model = parse_gpx(xml)
        return gpx_model


if __name__ == '__main__':
    gpx_model = main()
    pass
