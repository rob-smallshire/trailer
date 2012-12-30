from trailer.model.fieldtools import make, nullable, make_list

class Track:

    def __init__(self, name=None, comment=None, description=None, source=None,
                 links=None, number=None, classification=None,
                 extensions=None, segments=None):
        self._name = nullable(str)(name)
        self._comment = nullable(str)(comment)
        self._description = nullable(str)(description)
        self._source = nullable(str)(source)
        self._links = make(list)(links)

        self._number = nullable(int)(number)
        if self._number is not None:
            if self._number < 0:
                raise ValueError("GPS track number {0} cannot be negative")

        self._classification = nullable(str)(classification)
        self._extensions = make_list(extensions)
        self._segments = make_list(segments)

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

    @property
    def description(self):
        return self._description

    @property
    def source(self):
        return self._source

    @property
    def links(self):
        return self._links

    @property
    def number(self):
        return self._number

    @property
    def classification(self):
        return self._classification

    @property
    def extensions(self):
        return self._extensions

    @property
    def segments(self):
        return self._segments



