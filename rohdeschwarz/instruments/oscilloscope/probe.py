from ..mixins import scpi_method, scpi_property, ScpiMixin


class Probe(ScpiMixin):

    def __init__(self, oscilloscope, index):
        ScpiMixin.__init__(self, oscilloscope)
        self.oscilloscope = oscilloscope
        self.index        = index


    ac_coupling = scpi_property('PROB{self.index}:SET:ACC', type=bool)
