from ....mixins    import scpi_method, scpi_property, ScpiMixin
from .s_parameter import SParameter


class UserData(ScpiMixin):

    def __init__(self, vsg, source):
        ScpiMixin.__init__(self, vsg)
        self.vsg    = vsg
        self.source = source


    # list size (property, int, get only)
    size = scpi_property('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS:SIZE', type=int, read_only=True)
    __len__ = scpi_method('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS:SIZE?', return_type=int)


    # clear list (method)
    clear = scpi_method('SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS:CLEAR')


    # s-parameter (e.g. S1)
    # start from index 0 to match python nomenclature
    def __getitem__(self, index):
        return SParameter(self.vsg, self.source, index + 1)


    # apply (method)
    apply = scpi_method('SOUR{self.source.index}:CORR:FRES:RF:USER:APPL')
