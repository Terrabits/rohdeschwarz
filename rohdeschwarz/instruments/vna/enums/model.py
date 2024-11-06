from .string_enum_mixin import StringEnumMixin


class Model(StringEnumMixin):

    # R&S VNA Models
    ZVA     = 'ZVA'
    ZVB     = 'ZVB'
    ZVH     = 'ZVH'
    ZVL     = 'ZVL'
    ZVT     = 'ZVT'
    ZNA     = 'ZNA'
    ZNBT    = 'ZNBT'
    ZNB     = 'ZNB'
    ZNC     = 'ZNC'
    ZND     = 'ZND'
    ZNP     = 'ZNP'
    ZNLE    = 'ZNLE'
    ZNL     = 'ZNL'

    # unknown model
    UNKNOWN = ''


    def is_in(self, string):
        if self == Model.UNKNOWN:
            return False
        else:
            return string.upper().find(self.value) != -1
