from .string_enum_mixin import StringEnumMixin


class TouchstoneFormat(StringEnumMixin):


    # decibel magnitude, angle in degrees
    DB_DEGREES        = 'LOGP'

    # linear magnitude, angle in degrees
    MAGNITUDE_DEGREES = 'LINP'

    # real and imaginary parts
    REAL_IMAGINARY    = 'COMP'
