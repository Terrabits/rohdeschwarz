from ..genericinstrument import GenericInstrument
from ..mixins            import scpi_method, scpi_property, ScpiMixin
from .filesystem         import FileSystem
from .source             import Source


class Vsg(GenericInstrument, ScpiMixin):

    def __init__(self):
        GenericInstrument.__init__(self)
        ScpiMixin.__init__(self, self)
        self.file = FileSystem(self)


    def source(self, index=1):
        return Source(self, index)
