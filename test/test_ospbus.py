from   rohdeschwarz.test.mock.bus         import OspBus

import unittest
from   ddt      import ddt, data

@ddt
class TestOspBus(unittest.TestCase):
    def setUp(self):
        self.bus = OspBus()

    @data({'scpi': r'ROUT:CLOS (@F01A11(1001))', 'instr': 1, 'module': 11, 'switch': 1,  'state': 10},
          {'scpi': r'ROUT:CLOS (@F01A12(1011))', 'instr': 1, 'module': 12, 'switch': 11, 'state': 10},
          {'scpi': r'ROUT:CLOS (@F02A11(1001))', 'instr': 2, 'module': 11, 'switch': 1,  'state': 10},
          {'scpi': r'ROUT:CLOS (@F02A12(0511))', 'instr': 2, 'module': 12, 'switch': 11, 'state': 5})
    def test_write(self, data):
        self.bus.write(data['scpi'])
        self.assertEqual(self.bus.switches[data['instr']][data['module']][data['switch']], data['state'])

    @data({'scpi': [r'ROUT:CLOS? (@F01A11(0001))'], 'result': 1},
          {'scpi': [r'ROUT:CLOS? (@F01A11(0101))'], 'result': 0},
          {'scpi': [r'ROUT:CLOS? (@F02A11(0001))'], 'result': 1},
          {'scpi': [r'ROUT:CLOS? (@F01A12(0001))'], 'result': 1},
          {'scpi': [r'ROUT:CLOS? (@F02A12(0101))'], 'result': 0},
          {'scpi': [r'ROUT:CLOS? (@F02A12(0111))'], 'result': 0},
          {'scpi': [r'ROUT:CLOS (@F02A12(0511))', r'ROUT:CLOS? (@F02A12(0511))'], 'result': 1},
          {'scpi': [r'ROUT:CLOS (@F02A12(0511))', r'ROUT:CLOS? (@F02A12(0111))'], 'result': 0})
    def test_query(self, data):
        for i in data['scpi']:
            self.bus.write(i)
        self.assertEqual(int(self.bus.read()), data['result'])

    def test_timeout_ms(self):
        x = self.bus.timeout_ms + 1000
        self.bus.timeout_ms = x

if __name__ == '__main__':
    unittest.main()
