from ..mixins import scpi_method, scpi_property, ScpiMixin


class Source(ScpiMixin):

    def __init__(self, vsg, index):
        ScpiMixin.__init__(self, vsg)
        self.index = index


    # basic settings
    frequency_Hz    = scpi_property('SOUR{self.index}:FREQ:CW',          type=float)
    level_dBm       = scpi_property('SOUR{self.index}:POW:LEV:IMM:AMPL', type=float)
    level_offset_dB = scpi_property('SOUR{self.index}:POW:LEV:IMM:OFFS', type=float)
    rf_on           = scpi_property('OUTP{self.index}:STAT',             type=bool)

    # modulation
    modulation_on = scpi_property('SOUR{self.index}:MOD:ALL:STAT',    type=bool)
