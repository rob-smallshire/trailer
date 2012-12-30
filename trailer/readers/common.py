__author__ = 'rjs'

def optional_text(parent, tag):
    element = parent.find(tag)
    return element.text if element is not None else None