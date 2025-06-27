from ...mixins           import scpi_method, scpi_property, ScpiMixin
from .digital_modulation import DigitalModulation


class Baseband(ScpiMixin):

    def __init__(self, vsg, source):
        ScpiMixin.__init__(self, vsg)
        self.vsg    = vsg
        self.source = source


    @property
    def digital_modulation(self):
        return DigitalModulation(self.vsg, self.source)
