from ....mixins       import scpi_method, scpi_property, ScpiMixin
from .apply_decorator import apply
from .apply_property  import apply_property
from .s_parameter     import SParameter


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


    @apply
    def insert(self, index, touchstone_file):
        # bound index, matching expected python collection behavior
        if index < 0:
            index = 0
        if index > self.size:
            index = self.size

        # insert
        self.vsg.write(f"SOUR{self.source.index}:CORR:FRES:RF:USER:SLIS{index + 1}:SEL '{touchstone_file}'")


    def append(self, touchstone_file):
        self.insert(self.size, touchstone_file)


    # s-parameter (e.g. S1)
    # start from index 0 to match python nomenclature
    def __getitem__(self, index):
        self.raise_if_invalid_index(index)
        index = self.round_index(index)
        return SParameter(self.vsg, self.source, index + 1)


    def __delitem__(self, index):
        self.raise_if_invalid_index(index)
        index = self.round_index(index)
        for i in range(index, self.size - 1):
            s_i    = self[i]
            s_next = self[i+1]

            s_i.on              = s_next.on
            s_i.to_port         = s_next.to_port
            s_i.from_port       = s_next.from_port
            s_i.touchstone_file = s_next.touchstone_file

        self[-1].touchstone_file = 'None'


    # apply (method)
    apply = scpi_method('SOUR{self.source.index}:CORR:FRES:RF:USER:APPL')


    def raise_if_invalid_index(self, index):
        # index too large?
        if index >= self.size:
            raise IndexError('list index out of range')

        # index too negative?
        if index < 0:
            index = self.size - index
            if index < 0:
                raise IndexError('list index out of range')


    def round_index(self, index):
        if index < 0:
            # wrap index to end
            return self.size + index

        return index
