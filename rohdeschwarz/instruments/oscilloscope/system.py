from ..mixins import scpi_method, scpi_property, ScpiMixin


class System(ScpiMixin):

    def __init__(self, oscilloscope):
        ScpiMixin.__init__(self, oscilloscope)
        self.oscilloscope = oscilloscope


    # firmware upgrade

    firmware_path = scpi_property('SYST:FW:FIL', type=str)


    def upgrade_firmware(self, path):
        self.firmware_path = path
        self.oscilloscope.write('SYST:FW:STAR')
