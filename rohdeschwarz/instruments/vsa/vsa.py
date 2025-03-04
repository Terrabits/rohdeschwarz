from ..genericinstrument import GenericInstrument
from .filesystem         import FileSystem
from .properties         import Properties


class Vsa(GenericInstrument):


    def __init__(self):
        super(Vsa, self).__init__()


    @property
    def file(self):
        return FileSystem(self)


    @property
    def properties(self):
        return Properties(self)
