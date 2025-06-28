from ..genericinstrument import GenericInstrument
from ..mixins import scpi_method, scpi_property, ScpiMixin
from .channel            import Channel
from .filesystem         import FileSystem
from .properties         import Properties
from .frequency_response_corrections import FrequencyResponseCorrections


class Vsa(GenericInstrument, ScpiMixin):


    def __init__(self):
        GenericInstrument.__init__(self)
        ScpiMixin.__init__(self, self)


    @property
    def file(self):
        return FileSystem(self)


    @property
    def properties(self):
        return Properties(self)


    # operating mode
    operating_mode = scpi_property('INST:MODE')


    # channel

    create_channel = scpi_method("INST:CRE {type}, {name}", type=None, name=str)
    delete_channel = scpi_method("INST:DEL {name}", name=str)


    @property
    def channels(self):
        parts = self.query('INST:LIST?').strip().split(',')
        names = parts[1::2]
        return [i.strip("'") for i in names]


    def channel(self, name):
        return Channel(self, name)


    @property
    def channel_objects(self):
        return [Channel(self, name) for name in self.channels]


    @property
    def frequency_response_corrections(self):
        return FrequencyResponseCorrections(self)
