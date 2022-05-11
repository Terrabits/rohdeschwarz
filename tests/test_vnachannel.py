from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.test.mock.bus   import FifoBus

from ddt import ddt, data

import sys
import unittest

@ddt
class TestVnaChannel(unittest.TestCase):
    @data({'channel':   5,
           'port':      3,
           'sweeps':   13,
           'tolerance': 0.03,
           'reads': [
                'Rohde-Scharz,ZVA24-4Port,serialno,fwver',
                '1'
           ],
           'writes': [
                {'command': 'SOUR5:POW3:CORR:NRE 13'   },
                {'command': 'SOUR5:POW3:CORR:NTOL 0.03'},
                {'command': 'SOUR:POW:CORR:COLL:RREC 1'},
                {'command': 'SOUR5:POW:CORR:ACQ PORT,3', 'position': -2},
                {'command': '*OPC?',                     'position': -1}
            ]},
          {'channel':  10,
           'port':     10,
           'sweeps':    1,
           'tolerance': 1,
           'reads': [
                'Rohde-Scharz,ZNB8-4Port,serialno,fwver',
                '1'
         ],
         'writes': [
                {'command': 'SOUR10:POW10:CORR:NRE 1'  },
                {'command': 'SOUR10:POW10:CORR:NTOL 1' },
                {'command': 'SOUR10:POW:CORR:ACQ PORT,10', 'position': -2},
                {'command': '*OPC?',                       'position': -1}
          ]})
    def test_source_power_cal(self, data):
        reads     = data['reads']
        ch        = data['channel']
        port      = data['port']
        sweeps    = data['sweeps']
        tolerance = data['tolerance']

        vna = Vna()
        vna.bus = FifoBus(reads)
        vna.channel(ch).source_power_cal(port, sweeps, tolerance)
        for write in data['writes']:
            if 'position' in write:
                pos = write['position']
                self.assertEqual(write['command'], vna.bus.writes[pos])
            else:
                self.assertIn   (write['command'], vna.bus.writes)
