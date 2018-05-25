from   ddt                          import ddt, data
from   rohdeschwarz.instruments.vna import Vna
from   rohdeschwarz.test.mock.bus   import FifoBus
import unittest

@ddt
class TestVna(unittest.TestCase):
    @data({'read': '1,2,3,4', 'result': [1,2,3,4]},
          {'read': '1,2\n',   'result': [1,2    ]},
          {'read': '',        'result': [       ]})
    def test_power_sensors(self, data):
        vna     = Vna()
        vna.bus = FifoBus([data['read']])
        self.assertEqual(vna.power_sensors, data['result'])
