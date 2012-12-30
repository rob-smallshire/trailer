from lxml import etree

from trailer.readers.gpx_1_0.parser import parse_gpx as parse_gpx_1_0
from trailer.readers.gpx_1_1.parser import parse_gpx as parse_gpx_1_1


GPX = '{http://www.topografix.com/GPX/1/0}'

def parse_gpx(xml):
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
