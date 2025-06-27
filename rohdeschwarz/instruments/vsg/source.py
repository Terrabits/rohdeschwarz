from ..mixins  import scpi_method, scpi_property, ScpiMixin
from .baseband import Baseband
from .iq       import Iq


class Source(ScpiMixin):

    def __init__(self, vsg, index):
        ScpiMixin.__init__(self, vsg)
        self.vsg   = vsg
        self.index = index


    # basic settings
    frequency_Hz    = scpi_property('SOUR{self.index}:FREQ:CW',          type=float)
    level_dBm       = scpi_property('SOUR{self.index}:POW:LEV:IMM:AMPL', type=float)
    level_offset_dB = scpi_property('SOUR{self.index}:POW:LEV:IMM:OFFS', type=float)
    rf_on           = scpi_property('OUTP{self.index}:STAT',             type=bool)


    # baseband
    @property
    def baseband(self):
        return Baseband(self.vsg, self)


    @property
    def iq(self):
        return Iq(self.vsg, self)
