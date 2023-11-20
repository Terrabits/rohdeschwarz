from enum import Enum


class SweepType(str, Enum):


    LINEAR    = 'LIN'
    LOG       = 'LOG'
    SEGMENTED = 'SEGM'
    POWER     = 'POW'
    CW        = 'CW'
    TIME      = 'POIN'
