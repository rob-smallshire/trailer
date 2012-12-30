from trailer.model.fieldtools import nullable

class Person:

    def __init__(self, name=None, email=None, link=None):

        self._name = nullable(str)(name)
        self._email = nullable(str)(email)
        self._link = link

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def link(self):
        return self._link




