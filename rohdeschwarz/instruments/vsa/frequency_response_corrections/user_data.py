from ...mixins    import scpi_method, scpi_property, ScpiMixin
from .s_parameter import SParameter
from .scope       import ScopeMixin, scope_method, scope_property


class UserData(ScpiMixin, ScopeMixin):

    def __init__(self, vsa, channel):
        ScpiMixin.__init__(self, vsa)
        self.vsa    = vsa
        self.channel = channel


    # list size (property, int, get only)
    size    = scope_property(scpi_property('SENS:CORR:FRES:USER:SLIS:SIZE', type=int, read_only=True))
    __len__ = scope_method(scpi_method('SENS:CORR:FRES:USER:SLIS:SIZE?', return_type=int))


    # clear list (method)
    clear = scope_method(scpi_method('SENS:CORR:FRES:USER:SLIS:CLE'))


    # start from index 0 to match python nomenclature
    def insert(self, index, touchstone_file):
        # bound index, matching expected python collection behavior
        if index < 0:
            index = 0
        if index > self.size:
            index = self.size

        # insert
        self.vsa.write(f"SENS:CORR:FRES:USER:SLIS{index + 1}:INS '{touchstone_file}'")


    def append(self, touchstone_file):
        self.insert(self.size, touchstone_file)


    # get s-parameter (e.g. S1)
    # start from index 0 to match python nomenclature
    def __getitem__(self, index):
        self.raise_if_invalid_index(index)
        index = self.round_index(index)
        return SParameter(self.vsa, self.channel, index + 1)

    # delete s-parameter (e.g. S1)
    # start from index 0 to match python nomenclature
    def __delitem__(self, index):
        self.raise_if_invalid_index(index)
        index = self.round_index(index)
        self.vsa.write(f'SENS:CORR:FRES:USER:SLIS{index + 1}:REM')


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
