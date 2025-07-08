from ....mixins      import scpi_property, ScpiMixin
from .apply_property import apply_property


class SParameter(ScpiMixin):

    def __init__(self, vsg, source, index):
        ScpiMixin.__init__(self, vsg)
        self.vsg    = vsg
        self.source = source
        self.index  = index


    on        = apply_property(scpi_property('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS{self.index}:STAT', type=bool))
    to_port   = apply_property(scpi_property('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS{self.index}:PORT:TO',   type=int))
    from_port = apply_property(scpi_property('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS{self.index}:PORT:FROM', type=int))
    touchstone_file = apply_property(scpi_property('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS{self.index}:SEL', type=str))
