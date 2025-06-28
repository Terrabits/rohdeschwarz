from ....mixins import scpi_property


class ScopeMixin:

    # scope: ALL or CHAN
    scope = scpi_property("SENS:CORR:FRES:USER:SCOP")


    @property
    def is_channel_specific(self):
        return self.channel is not None


    def set_scope(self):
        if self.is_channel_specific:
            self.scope = 'CHAN'
        else:
            self.scope = 'ALL'
