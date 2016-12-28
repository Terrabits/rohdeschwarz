import unittest
from   ddt      import ddt, data
from rohdeschwarz.general         import Units
from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.instruments.vna import TraceFormat
from rohdeschwarz.instruments.vna import VnaTrace

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

    @data({'param': 'S11',       'type': 'reg_s', 'ports': [1]},
          {'param': 'Y21',       'type': 'reg_s', 'ports': [1, 2]},
          {'param': 'Z32',       'type': 'reg_s', 'ports': [2, 3]},
          {'param': 'Sdd11',     'type': 'reg_b', 'ports': [1]},
          {'param': 'Sdc11',     'type': 'reg_b', 'ports': [1]},
          {'param': 'Scd21',     'type': 'reg_b', 'ports': [1, 2]},
          {'param': 'Scc12',     'type': 'reg_b', 'ports': [1, 2]},
          {'param': 'Sss22',     'type': 'reg_b', 'ports': [2]},
          {'param': 'Zsd31',     'type': 'reg_b', 'ports': [1, 3]},
          {'param': 'Zds13',     'type': 'reg_b', 'ports': [1, 3]},
          {'param': 'Ysc0101',   'type': 'reg_b', 'ports': [1]},
          {'param': 'Ycs0102',   'type': 'reg_b', 'ports': [1, 2]},
          {'param': 'Z-S0201',   'type': 'imp',   'ports': [1, 2]},
          {'param': 'Y-Sdd0202', 'type': 'adm',   'ports': [2]},
          {'param': 'A1D1SAM',   'type': 'wave',  'ports': [1]},
          {'param': 'B1D1AVG',   'type': 'wave',  'ports': [1]},
          {'param': 'A2G2AMP',   'type': 'wave',  'ports': [2]},
          {'param': 'A1D1/B1D2AVG',     'type': 'wave_r', 'ports': [1]},
          {'param': 'A2G1/B1D1SAM',     'type': 'wave_r', 'ports': [1, 2]})
    def test_parse_params(self, data):
        # type
        self.assertEqual(VnaTrace._is_wave(data['param']),                   data['type'] == 'wave')
        self.assertEqual(VnaTrace._is_wave_ratio(data['param']),             data['type'] == 'wave_r')
        self.assertEqual(VnaTrace._is_impedance(data['param']),              data['type'] == 'imp')
        self.assertEqual(VnaTrace._is_admittance(data['param']),             data['type'] == 'adm')
        self.assertEqual(VnaTrace._is_regular_param(data['param']),          data['type'][0:3] == 'reg')
        self.assertEqual(VnaTrace._is_regular_single_param(data['param']),   data['type'] == 'reg_s')
        self.assertEqual(VnaTrace._is_regular_balanced_param(data['param']), data['type'] == 'reg_b')

        # ports
        if data['type'] == 'wave':
            port = VnaTrace._parse_wave_port(data['param'])
            self.assertEqual([port], data['ports'])
        if data['type'] == 'wave_r':
            ports = VnaTrace._parse_wave_ratio_ports(data['param'])
            self.assertEqual(ports, data['ports'])
        if data['type'] == 'imp':
            ports = VnaTrace._parse_impedance_ports(data['param'])
            self.assertEqual(ports, data['ports'])
        if data['type'] == 'adm':
            ports = VnaTrace._parse_admittance_ports(data['param'])
            self.assertEqual(ports, data['ports'])
        if data['type'][0:3] == 'reg':
            ports = VnaTrace._parse_regular_param_ports(data['param'])
            self.assertEqual(ports, data['ports'])

    @data({'digits': '21',     'result': [1, 2]},
          {'digits': '1234',   'result': [12, 34]},
          {'digits': '123456', 'result': [123, 456]})
    def test_parse_two_digits(self, data):
        result = VnaTrace._parse_two_digits(data['digits'])
        self.assertEqual(result, data['result'])

if __name__ == '__main__':
    unittest.main()
