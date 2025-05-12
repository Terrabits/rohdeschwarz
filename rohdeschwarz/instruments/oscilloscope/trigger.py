from .event   import Event
from ..mixins import scpi_method, scpi_property, ScpiMixin


class Trigger(ScpiMixin):

    def __init__(self, oscilloscope):
        ScpiMixin.__init__(self, oscilloscope)
        self.oscilloscope = oscilloscope


    def event(self, index=1):
        return Event(self.oscilloscope, index)
