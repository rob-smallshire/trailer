from trailer.model.fieldtools import nullable

class Link:
    """A link to an external resource (Web page, digital photo, video clip,
    etc) with additional information."""

    def __init__(self, href, text=None, mime=None):
        self._href = str(href)
        self._text = nullable(str)(text)
        self._mime = nullable(str)(mime)

    @property
    def href(self):
        return self._href

    @property
    def text(self):
        return self._text

    @property
    def mime(self):
        return self._mime
