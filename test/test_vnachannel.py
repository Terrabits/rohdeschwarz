from rohdeschwarz.instruments.vna import Vna

from ddt import ddt, data

import sys
import unittest

@ddt
class TestVnaChannel(unittest.TestCase):
    def test_save_measurement_locally(self):
        vna = Vna()
        vna.open_tcp('rsa22471.local')
        vna.preset()
        ports = [int(i) for i in range(1, vna.test_ports + 1)]
        ch = vna.channel()
        try:
            success = ch.save_measurement_locally('test.s4p', ports)
        except:
            print(sys.exc_info()[0])
            print(vna.errors)
            raise
        if not success:
            print(vna.errors)
            vna.clear_status()
        self.assertTrue(success)
