from enum import Enum


class Directory(str, Enum):
    DEFAULT        = 'DEF'
    EMBED          = 'Embedding'
    DEEMBED        = 'Deembedding'
    CAL_GROUPS     = 'Calibration\\Data'
    CAL_KITS       = 'Calibration\\Kits'
    EXTERNAL_TOOLS = 'External Tools'
    RECALL_SETS    = 'RecallSets'
    TRACES         = 'Traces'
