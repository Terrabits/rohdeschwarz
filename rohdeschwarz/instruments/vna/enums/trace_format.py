from .string_enum_mixin import StringEnumMixin
from rohdeschwarz.general import Units


class TraceFormat(StringEnumMixin):

    # trace formats
    magnitude_dB = 'MLOG'
    phase_deg    = 'PHAS'
    smith_chart  = 'SMIT'
    polar        = 'POL'
    vswr         = 'SWR'
    unwrapped_phase_deg = 'UPH'
    magnitude    = 'MLIN'
    inverse_smith_chart = 'ISM'
    real         = 'REAL'
    imaginary    = 'IMAG'
    group_delay  = 'GDEL'


    def __eq__(self, other):
        # compare case-insensitive
        return str(self).lower() == str(other).lower()


    def units(self):
        # These references to TraceFormat.enum
        # do not work in python 3-3.4 for some
        # reason. I can't find a way to reference
        # the enums inside a member method!
        return {
            self.magnitude_dB.value:        Units.dB,
            self.phase_deg.value:           Units.deg,
            self.smith_chart.value:         Units.ohms,
            self.polar.value:               Units.none,
            self.vswr.value:                Units.none,
            self.unwrapped_phase_deg.value: Units.deg,
            self.magnitude.value:           Units.none,
            self.inverse_smith_chart.value: Units.siemens,
            self.real.value:                Units.none,
            self.imaginary.value:           Units.none,
            self.group_delay.value:         Units.seconds
        }.get(self.value, self.magnitude_dB.value)
