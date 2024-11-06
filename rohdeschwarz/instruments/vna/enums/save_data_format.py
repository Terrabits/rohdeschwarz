from .string_enum_mixin import StringEnumMixin


class SaveDataFormat(StringEnumMixin):

    REAL_IMAGINARY    = 'COMP'
    DB_DEGREES        = 'LOGP'
    MAGNITUDE_DEGREES = 'LINP'
