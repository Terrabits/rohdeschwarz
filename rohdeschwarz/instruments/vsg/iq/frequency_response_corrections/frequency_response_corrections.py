from ....mixins import scpi_method, scpi_property, ScpiMixin
from .user_data import UserData


class FrequencyResponseCorrections(ScpiMixin):

    def __init__(self, vsg, source):
        ScpiMixin.__init__(self, vsg)
        self.vsg    = vsg
        self.source = source


    # state (property, bool)
    on = scpi_property('SOUR{self.source.index}:CORR:FRES:RF:USER:STAT', type=bool)


    # preset (set to default)
    preset = scpi_method('SOUR{self.source.index}:CORR:FRES:RF:USER:PRES')


    # user data s-parameters
    @property
    def user_data(self):
        return UserData(self.vsg, self.source)
