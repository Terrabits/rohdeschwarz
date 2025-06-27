from ...mixins import scpi_method, scpi_property, ScpiMixin
from .frequency_response_corrections import FrequencyResponseCorrections


class Iq(ScpiMixin):

    def __init__(self, vsg, source):
        ScpiMixin.__init__(self, vsg)
        self.vsg    = vsg
        self._source = source


    # state
    on = scpi_property('SOUR{self._source.index}:MOD:ALL:STAT', type=bool)


    # sources: BASeband, ANALog, DIFFerential
    source = scpi_property('SOUR{self._source.index}:IQ:SOUR')


    # frequency response corrections (SMW-K554)
    @property
    def frequency_response_corrections(self):
        return FrequencyResponseCorrections(self.vsg, self._source)
