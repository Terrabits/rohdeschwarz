from enum import Enum

class Model(Enum):
    zva  = 'ZVA'
    zvb  = 'ZVB'
    zvh  = 'ZVH'
    zvl  = 'ZVL'
    zvt  = 'ZVT'
    zna  = 'ZNA'
    znbt = 'ZNBT'
    znb  = 'ZNB'
    znc  = 'ZNC'
    znd  = 'ZND'
    znp  = 'ZNP'
    znle = 'ZNLE'
    znl  = 'ZNL'
    unknown = ''

    def __str__(self):
        return self.value

    def is_in(self, string):
        if self == Model.unknown:
            return False
        else:
            return string.upper().find(self.value) != -1


class Properties(object):
    def __init__(self, vna):
        super(Properties, self).__init__()
        self._vna = vna

    def is_znx(self):
        id = self._vna.id_string()
        if Model.zna.is_in(id):
            return True
        if Model.znbt.is_in(id):
            return True
        if Model.znb.is_in(id):
            return True
        if Model.znc.is_in(id):
            return True
        if Model.znd.is_in(id):
            return True
        if Model.znp.is_in(id):
            return True
        # else: not known znx model
        return False

    def is_zvx(self):
        id = self._vna.id_string()
        if Model.zva.is_in(id):
            return True
        elif Model.zvb.is_in(id):
            return True
        elif Model.zvh.is_in(id):
            return True
        elif Model.zvl.is_in(id):
            return True
        elif Model.zvt.is_in(id):
            return True
        else:
            return False

    def _model(self):
        id = self._vna.id_string()
        for model in Model:
            if (model.is_in(id)):
                return model
        return Model.unknown

    model = property(_model)

    def is_known_model(self):
        return self.is_znx() or self.is_zvx()

    def _serial_number(self):
        id_list = self._vna.id_string().strip().split(',');
        if len(id_list) < 3:
            return None
        else:
            return id_list[2].strip();

    serial_number = property(_serial_number)

    def _firmware_version(self):
        id_list = self._vna.id_string().strip().split(',');
        if len(id_list) < 4:
            return None
        else:
            return id_list[3].strip();

    firmware_version = property(_firmware_version)

    def _options_list(self):
        return self._vna.options_string().strip().split(',')

    options_list = property(_options_list)

    def _physical_ports(self):
        result = self._vna.query(':INST:PORT:COUN?')
        return int(result.strip())
    physical_ports = property(_physical_ports)

    def _minimum_frequency_Hz(self):
        result = self._vna.query(':SYST:FREQ? MIN').strip()
        return float(result)

    minimum_frequency_Hz = property(_minimum_frequency_Hz)

    def _maximum_frequency_Hz(self):
        result = self._vna.query(':SYST:FREQ? MAX').strip()
        return float(result)

    maximum_frequency_Hz = property(_maximum_frequency_Hz)

    def _minimum_power_dBm(self):
        if self.is_zvx():
            return -150
        elif self.is_znx:
            return -40
        else:
            return -40

    minimum_power_dBm = property(_minimum_power_dBm)

    def _maximum_power_dBm(self):
        if self.is_zvx():
            return 100
        elif self.is_znx():
            return 10
        else:
            return 10

    maximum_power_dBm = property(_maximum_power_dBm)

    def _maximum_points(self):
        if self.is_zvx():
            return 60001
        if self.is_znx():
            return 100001
        else:
            return 60001

    maximum_points = property(_maximum_points)
