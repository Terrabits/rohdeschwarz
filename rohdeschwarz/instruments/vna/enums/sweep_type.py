from .string_enum_mixin import StringEnumMixin


class SweepType(StringEnumMixin):


    LINEAR    = 'LIN'
    LOG       = 'LOG'
    SEGMENTED = 'SEGM'
    POWER     = 'POW'
    CW        = 'CW'
    TIME      = 'POIN'
