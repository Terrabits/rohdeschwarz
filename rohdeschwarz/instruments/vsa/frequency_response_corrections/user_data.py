from ...mixins    import scpi_method, scpi_property, ScpiMixin
from .s_parameter import SParameter
from .scope       import ScopeMixin, scope_method, scope_property


class UserData(ScpiMixin, ScopeMixin):

    def __init__(self, vsa, channel):
        ScpiMixin.__init__(self, vsa)
        self.vsa    = vsa
        self.channel = channel


    # list size (property, int, get only)
    size = scope_property(scpi_property
    (
        'SENS:CORR:FRES:USER:SLIS:SIZE',
        type=int,
        read_only=True
    ))
    __len__ = size


    # clear list (method)
    clear = scope_method(scpi_method('SENS:CORR:FRES:USER:SLIS:CLE'))


    # s-parameter (e.g. S1)
    # start from index 0 to match python nomenclature
    def __getitem__(self, index):
        return SParameter(self.vsa, self.channel, index + 1)
