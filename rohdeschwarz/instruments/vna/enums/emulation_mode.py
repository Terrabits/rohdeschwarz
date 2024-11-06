from .string_enum_mixin import StringEnumMixin


class EmulationMode(StringEnumMixin):


    # emulation modes
    PNA     = 'PNA'
    ENA     = 'ENA'
    HP_8510 = 'HP8510'
    HP_8530 = 'HP8530'
    HP_8720 = 'HP8720'
    HP_8753 = 'HP8753'
    HP_8714 = 'HP8714'
    ZVR     = 'ZVR'
    ZVABT   = 'ZVABT'

    # emulation off
    OFF     = 'SCPI'


    # should evaluate to true if emulation mode is on, false otherwise
    def __bool__(self):
        return not self == EmulationMode.OFF
