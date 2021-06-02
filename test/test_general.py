from ddt import ddt, data
from rohdeschwarz.enums   import SiPrefix, Units
from rohdeschwarz.instruments.vna import Vna
import unittest


@ddt
class TestGeneral(unittest.TestCase):
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
