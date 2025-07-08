from ..mixins import scpi_method, scpi_property, ScpiMixin
from .frequency_response_corrections import FrequencyResponseCorrections


class Channel(ScpiMixin):

    def __init__(self, vsa, name):
        ScpiMixin.__init__(self, vsa)
        self.vsa  = vsa
        self.name = name


    def __repr__(self):
        return f"Channel(name='{self.name}')"


    # select this channel (make active channel)
    select = scpi_method("INST:SEL '{self.name}'")


    # rename channel

    _rename_scpi_method = scpi_method("INST:REN '{self.name}', {new_name}", new_name=str)

    def rename(self, new_name):
        self._rename_scpi_method(new_name)
        self.name = new_name


    @property
    def frequency_response_corrections(self):
        return FrequencyResponseCorrections(self.vsa, channel=self)
