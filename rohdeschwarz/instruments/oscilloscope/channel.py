from .probe   import Probe
from ..mixins import scpi_method, scpi_property, ScpiMixin


class Channel(ScpiMixin):

    def __init__(self, oscilloscope, index):
        ScpiMixin.__init__(self, oscilloscope)
        self.oscilloscope = oscilloscope
        self.index        = index
        self.probe        = Probe(oscilloscope, index)


    # power calculation
    impedance_ohms = scpi_property('CHAN{self.index}:IMP', type=float)
