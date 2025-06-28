from ...mixins    import scpi_method, scpi_property, ScpiMixin
from .scope       import ScopeMixin, scope_method, scope_property
from .user_data   import UserData


class FrequencyResponseCorrections(ScpiMixin, ScopeMixin):

    def __init__(self, vsa, channel=None):
        ScpiMixin.__init__(self, vsa)
        self.vsa     = vsa
        self.channel = channel


    # state (property, bool)
    on = scope_property(scpi_property('SENS:CORR:FRES:USER:STAT', type=bool))


    # preset (method)
    preset = scope_method(scpi_method('SENS:CORR:FRES:USER:PRES'))


    # user data s-parameters
    @property
    def user_data(self):
        return UserData(self.vsa, self.channel)
