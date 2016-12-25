import unittest
from   ddt      import ddt, data
from rohdeschwarz.general         import Units
from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.instruments.vna import TraceFormat

@ddt
class TestVnaTrace(unittest.TestCase):
    @data({'enum': TraceFormat.magnitude_dB,        'units': Units.dB},
          {'enum': TraceFormat.phase_deg,           'units': Units.deg},
          {'enum': TraceFormat.smith_chart,         'units': Units.ohms},
          {'enum': TraceFormat.polar,               'units': Units.none},
          {'enum': TraceFormat.vswr,                'units': Units.none},
          {'enum': TraceFormat.unwrapped_phase_deg, 'units': Units.deg},
          {'enum': TraceFormat.magnitude,           'units': Units.none},
          {'enum': TraceFormat.inverse_smith_chart, 'units': Units.siemens},
          {'enum': TraceFormat.real,                'units': Units.none},
          {'enum': TraceFormat.imaginary,           'units': Units.none},
          {'enum': TraceFormat.group_delay,         'units': Units.seconds})
    def test_trace_format_units(self, data):
        self.assertEqual(data['enum'].units(), data['units'])

if __name__ == '__main__':
    unittest.main()
