import unittest
from   ddt      import ddt, data
from rohdeschwarz.general         import Units, format_value
from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.instruments.vna import TraceFormat

@ddt
class TestGeneral(unittest.TestCase):
    @data({'value': 0.5,    'units': Units.dB,      'result': '0.5 dB'},
          {'value': 5.0e-9, 'units': Units.seconds, 'result': '5.0 ns'},
          {'value': 10.0,   'units': Units.none,    'result': '10.0 U'})
    def test_trace_format_units(self, data):
        self.assertEqual(format_value(data['value'], data['units']), data['result'])

if __name__ == '__main__':
    unittest.main()
