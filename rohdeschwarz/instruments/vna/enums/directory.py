from .string_enum_mixin import StringEnumMixin


class Directory(StringEnumMixin):
    DEFAULT        = 'DEF'
    EMBED          = 'Embedding'
    DEEMBED        = 'Deembedding'
    CAL_GROUPS     = 'Calibration\\Data'
    CAL_KITS       = 'Calibration\\Kits'
    EXTERNAL_TOOLS = 'External Tools'
    RECALL_SETS    = 'RecallSets'
    TRACES         = 'Traces'
