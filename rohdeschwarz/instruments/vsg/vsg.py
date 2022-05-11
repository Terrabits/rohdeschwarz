from rohdeschwarz.instruments.instrument import Instrument
from rohdeschwarz.instruments.vsg.filesystem    import FileSystem

class Vsg(Instrument):
    def __init__(self):
        Instrument.__init__(self)
        self.file = FileSystem(self)
