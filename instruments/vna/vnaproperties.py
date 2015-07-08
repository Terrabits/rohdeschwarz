from enum import Enum

class Model(Enum):
    zva  = 'ZVA'
    zvb  = 'ZVB'
    zvh  = 'ZVH'
    zvl  = 'ZVL'
    zvt  = 'ZVT'
    znbt = 'ZNBT'
    znb  = 'ZNB'
    znc  = 'ZNC'
    znd  = 'ZND'
    znp  = 'ZNP'
    unknown = ''

    def __str__(self):
        return self.value

    def is_in(self, string):
        if self == Model.unknown:
            return False
        else:
            return string.upper().find(self.value) != -1


class VnaProperties:
    def __init__(self, vna):
        self._vna = vna

    def is_znb_family(self):
        id = self._vna.id_string()
        if Model.znb.is_in(id):
            return True
        elif Model.znbt.is_in(id):
            return True
        elif Model.znc.is_in(id):
            return True
        elif Model.znd.is_in(id):
            return True
        elif Model.znp.is_in(id):
            return True
        else:
            return False

    def is_zva_family(self):
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
        return self.is_znb_family() or self.is_zva_family()

    def _physical_ports(self):
        result = self._vna.query(':INST:PORT:COUN?')
        return int(result.strip())

    physical_ports = property(_physical_ports)

