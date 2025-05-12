from ..mixins import scpi_method, scpi_property, ScpiMixin


class Event(ScpiMixin):

    def __init__(self, oscilloscope, index):
        ScpiMixin.__init__(self, oscilloscope)
        self.oscilloscope = oscilloscope
        self.index        = index


    source      = scpi_property('TRIG:EVEN{self.index}:SOUR')
    type        = scpi_property('TRIG:EVEN{self.index}:TYPE')
    edge_slope  = scpi_property('TRIG:EVEN{self.index}:EDGE:SLOP')


    # level, per channel

    def level(self, channel):
        scpi = f'TRIG:EVEN{self.index}:LEV{channel}?'
        result = self.oscilloscope.query(scpi)
        return float(result)


    def setLevel(self, channel, value):
        scpi = f'TRIG:EVEN{self.index}:LEV{channel} {value}'
        self.oscilloscope.write(scpi)
