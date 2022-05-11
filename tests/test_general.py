from rohdeschwarz.general         import format_value
from rohdeschwarz.general         import SiPrefix
from rohdeschwarz.general         import to_float
from rohdeschwarz.general         import Units
from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.instruments.vna import TraceFormat

from   ddt      import ddt, data

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

	@data({'args': (10.0),              'value': 10.0},
		  {'args': ('10.0'),            'value': 10.0},
		  {'args': ('10 MHz'),          'value': 10e6},
		  {'args': (99, SiPrefix.mega), 'value': 99e6})
	def test_to_float(self, data):
		args = data['args']
		if isinstance(args, tuple):
			self.assertEqual(to_float(*args), data['value'])
		else:
			self.assertEqual(to_float(args), data['value'])

if __name__ == '__main__':
	unittest.main()
