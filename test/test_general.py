from ddt import ddt, data
from rohdeschwarz.helpers import SiPrefix
from rohdeschwarz.enums   import Units
from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.instruments.vna import TraceFormat
import unittest


@ddt
class TestGeneral(unittest.TestCase):
	@data({'value': 0.5,    'units': Units.dB,      'result': '0.5 dB'},
		  {'value': 5.0e-9, 'units': Units.seconds, 'result': '5 ns'},
		  {'value': 10.0,   'units': Units.none,    'result': '10 U'})
	def test_trace_format_units(self, data):
		self.assertEqual(format_value(data['value'], data['units']), data['result'])

	@data({'value':  10.0,     'num': 10.0, 'prefix': SiPrefix.none},
		  {'value': '10.0',    'num': 10.0, 'prefix': SiPrefix.none},
		  {'value': '10e6',    'num': 10.0, 'prefix': SiPrefix.mega},
		  {'value': '37 ps',   'num': 37.0, 'prefix': SiPrefix.pico})
	def test_si_prefix_convert(self, data):
		num, prefix = SiPrefix.convert(data['value'])
		self.assertEqual(data['num'], num)
		self.assertEqual(data['prefix'], prefix)

if __name__ == '__main__':
	unittest.main()
