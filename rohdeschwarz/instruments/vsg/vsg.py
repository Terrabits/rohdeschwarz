from rohdeschwarz.instruments.genericinstrument import GenericInstrument
from rohdeschwarz.instruments.vsg.filesystem    import FileSystem

class Vsg(GenericInstrument):
    def __init__(self):
        GenericInstrument.__init__(self)
        self.file = FileSystem(self)
