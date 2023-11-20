from enum import Enum


class SaveDataFormat(str, Enum):

    REAL_IMAGINARY    = 'COMP'
    DB_DEGREES        = 'LOGP'
    MAGNITUDE_DEGREES = 'LINP'
