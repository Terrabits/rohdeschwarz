from ...mixins import scpi_property, ScpiMixin
from .scope    import ScopeMixin, scope_property


class SParameter(ScpiMixin, ScopeMixin):

    def __init__(self, vsa, channel, index):
        ScpiMixin.__init__(self, vsa)
        self.vsa     = vsa
        self.channel = channel
        self.index   = index


    # properties
    on        = scope_property(scpi_property('SENS:CORR:FRES:USER:SLIS{self.index}:STAT',      type=bool))
    to_port   = scope_property(scpi_property('SENS:CORR:FRES:USER:SLIS{self.index}:PORT:TO',   type=int))
    from_port = scope_property(scpi_property('SENS:CORR:FRES:USER:SLIS{self.index}:PORT:FROM', type=int))
    touchstone_file = scope_property(scpi_property('SENS:CORR:FRES:USER:SLIS{self.index}:SEL', type=str))
    valid     = scope_property(scpi_property('SENS:CORR:FRES{self.index}:USER:VAL', type=bool, read_only=True))
