from ...mixins  import scpi_method, scpi_property, ScpiMixin


class DigitalModulation(ScpiMixin):

    def __init__(self, vsg, source):
        ScpiMixin.__init__(self, vsg)
        self.vsg    = vsg
        self.source = source


    on = scpi_property('SOUR{self.source.index}:BB:DM:STAT', type=bool)
