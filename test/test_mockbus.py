from   rohdeschwarz.test.mock.bus.base import MockBus
from   ddt import ddt, data
import unittest

@ddt
class TestMockBus(unittest.TestCase):
    def setUp(self):
        self.bus = MockBus()

    def test_id_string(self):
        self.bus.write('*IDN?')
        self.assertTrue(self.bus.read())
    def test_opc(self):
        self.bus.write('*OPC?')
        self.assertEqual(self.bus.read(), '1')
    def test_timeout_ms(self):
        x = self.bus.timeout_ms + 1000
        self.bus.timeout_ms = x

if __name__ == '__main__':
    unittest.main()
