__author__ = 'rjs'

def optional_text(parent, tag):
    element = parent.find(tag)
    return element.text if element is not None else None


def determine_gpx_namespace(gpx_element):
    gpxns = '{' + gpx_element.nsmap.get(None, '') + '}'
    if not gpxns.startswith('{http://www.topografix.com/GPX'):
        raise ValueError("Unrecognised GPX namespace '{0}'".format(gpxns))
    return gpxns