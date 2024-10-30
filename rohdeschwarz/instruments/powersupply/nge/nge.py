from ...genericinstrument import GenericInstrument
from .channel            import Channel



class Nge(GenericInstrument):


    # constructor
    def __init__(self):
        GenericInstrument.__init__(self)


    # channel
    def channel(self, index=1):
        return Channel(self, index)
