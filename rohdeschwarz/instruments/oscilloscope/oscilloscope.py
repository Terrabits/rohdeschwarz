from .channel            import Channel
from .system             import System
from .trigger            import Trigger
from ..genericinstrument import GenericInstrument
from ..mixins            import scpi_method, scpi_property, ScpiMixin


class Oscilloscope(GenericInstrument, ScpiMixin):

    def __init__(self):
        GenericInstrument.__init__(self)
        ScpiMixin.__init__(self, self)
        self.system  = System(self)
        self.trigger = Trigger(self)


    def channel(self, index=1):
        return Channel(self, index)


    # acquisition
    average_count = scpi_property('ACQ:COUN', type=int)
