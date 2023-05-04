from   .limits     import Limits
from   .marker     import Marker
from   .preserve_data_transfer_settings import PreserveDataTransferSettings
from   .timedomain import TimeDomain
import csv
from   enum    import Enum
import numpy
from   pathlib import Path
import re
from   rohdeschwarz.general import unique_alphanumeric_string
from   rohdeschwarz.general import Units
import sys


class TraceFormat(Enum):
    magnitude_dB = 'MLOG'
    phase_deg    = 'PHAS'
    smith_chart  = 'SMIT'
    polar        = 'POL'
    vswr         = 'SWR'
    unwrapped_phase_deg = 'UPH'
    magnitude    = 'MLIN'
    inverse_smith_chart = 'ISM'
    real         = 'REAL'
    imaginary    = 'IMAG'
    group_delay  = 'GDEL'
    def units(self):
        # These references to TraceFormat.enum
        # do not work in python 3-3.4 for some
        # reason. I can't find a way to reference
        # the enums inside a member method!
        return {
            self.magnitude_dB.value:        Units.dB,
            self.phase_deg.value:           Units.deg,
            self.smith_chart.value:         Units.ohms,
            self.polar.value:               Units.none,
            self.vswr.value:                Units.none,
            self.unwrapped_phase_deg.value: Units.deg,
            self.magnitude.value:           Units.none,
            self.inverse_smith_chart.value: Units.siemens,
            self.real.value:                Units.none,
            self.imaginary.value:           Units.none,
            self.group_delay.value:         Units.seconds
        }.get(self.value, self.magnitude_dB.value)
    def __str__(self):
        return self.value
    def __eq__(self, other):
        return self.value.lower() == str(other).lower()


class SaveDataFormat(Enum):
    real_imaginary = 'COMP'
    dB_degrees = 'LOGP'
    magnitude_degrees = 'LINP'
    def __str__(self):
        return self.value


class Trace(object):
    def __init__(self, vna, name='Trc1'):
        super(Trace, self).__init__()
        self._vna = vna
        self.name = name

    def select(self):
        scpi = ":CALC{0}:PAR:SEL '{1}'"
        scpi = scpi.format(self.channel, self.name)
        self._vna.write(scpi)

    def _channel(self):
        scpi = ":CONF:TRAC:CHAN:NAME:ID? '{0}'"
        scpi = scpi.format(self.name)
        result = self._vna.query(scpi).strip().strip("'")
        return int(result)
    def _set_channel(self, index):
        sys.stderr.write("Cannot change trace's channel via SCPI\n")
    channel = property(_channel, _set_channel)

    def _diagram(self):
        if self._vna.properties.is_zvx():
            diagrams = self._vna.diagrams
            for d in diagrams:
                traces = self._vna.diagram(d).traces
                if self.name in traces:
                    return d
            return None
        else:
            scpi = ":CONF:TRAC:WIND? '{0}'"
            scpi = scpi.format(self.name)
            result = self._vna.query(scpi).strip()
            return int(result)
    def _set_diagram(self, index):
        scpi = ":DISP:WIND{0}:TRAC:EFE '{1}'"
        scpi = scpi.format(index, self.name)
        self._vna.write(scpi)
    diagram = property(_diagram, _set_diagram)

    def _parameter(self):
        scpi = ":CALC{0}:PAR:MEAS? '{1}'"
        scpi = scpi.format(self.channel, self.name)
        result = self._vna.query(scpi).strip()
        result = result.replace("'","")
        return result
    def _set_parameter(self, value):
        scpi = ":CALC{0}:PAR:MEAS '{1}','{2}'"
        scpi = scpi.format(self.channel, self.name, value)
        self._vna.write(scpi)
    parameter = property(_parameter, _set_parameter)

    def _format(self):
        scpi = ':CALC{0}:FORM?'
        scpi = scpi.format(self.channel)
        self.select()
        result = self._vna.query(scpi).strip()
        return TraceFormat(result)
    def _set_format(self, value):
        scpi = ':CALC{0}:FORM {1}'
        scpi = scpi.format(self.channel, value)
        self.select()
        self._vna.write(scpi)
    format = property(_format, _set_format)

    def y_units(self):
        param = self.parameter.lower()
        fmt   = self.format
        if fmt == TraceFormat.magnitude:
            if param[0] == 'z':
                return Units.ohms
            if param[0] == 'y':
                return Units.siemens
        if param[0:2] == 'dc':
            if fmt  == TraceFormat.magnitude:
                return Units.v
            if fmt == TraceFormat.magnitude_dB:
                return Units.dBuV
            if fmt == TraceFormat.polar:
                return Units.v
        if param[0] == 'a' or param[0] == 'b' and not '/' in param:
            if fmt == TraceFormat.magnitude_dB:
                return Units.dBm
            if fmt == TraceFormat.magnitude:
                return Units.mW
            if fmt == TraceFormat.polar:
                return Units.mW
            if fmt == TraceFormat.real or fmt == TraceFormat.imaginary:
                return Units.mW
        # else
        return fmt.units()
    def x_units(self):
        if self.time_domain.on:
            return Units.seconds
        # else
        ch = self._vna.channel(self.channel)
        return ch.x_units()

    def autoscale(self):
        scpi = ":DISP:TRAC:Y:AUTO ONCE, '{0}'"
        scpi = scpi.format(self.name)
        self._vna.write(scpi)

    def _x(self):
        self.select();
        scpi = ":CALC{0}:DATA:STIM?"
        scpi = scpi.format(self.channel)
        data_format = self._vna.settings.data_format
        self._vna.settings.binary_64_bit_data_format = True
        self._vna.write(scpi)
        stimulus_data = self._vna.read_64_bit_vector_block_data()
        self._vna.settings.data_format = data_format
        return stimulus_data
    x = property(_x)

    def _y_complex(self):
        channel = self._vna.channel(self.channel)
        if self._vna.properties.is_zvx():
            self.select()
            scpi = ':CALC{0}:DATA? SDAT'
            scpi = scpi.format(channel.index)
        else:
            scpi = ":CALC:DATA:TRAC? '{0}', SDAT"
            scpi = scpi.format(self.name)
        self._vna.pause(2 * channel.sweep_time_ms * channel.sweep_count + 5000)
        data_format = self._vna.settings.data_format
        self._vna.settings.binary_64_bit_data_format = True
        self._vna.write(scpi)
        result = self._vna.read_64_bit_complex_vector_block_data()
        self._vna.settings.data_format = data_format
        return result
    y_complex = property(_y_complex)

    def _y_formatted(self):
        channel = self._vna.channel(self.channel)
        if self._vna.properties.is_zvx():
            self.select()
            scpi = ':CALC{0}:DATA? FDAT'
            scpi = scpi.format(channel.index)
        else:
            scpi = ":CALC:DATA:TRAC? '{0}', FDAT"
            scpi = scpi.format(self.name)
        data_format = self._vna.settings.data_format
        self._vna.settings.binary_64_bit_data_format = True
        self._vna.write(scpi)
        result = self._vna.read_64_bit_vector_block_data()
        self._vna.settings.data_format = data_format
        self._vna.settings.data_format = data_format
        return result
    y_formatted = property(_y_formatted)


    # trace history

    @property
    def complex_history(self):
        """
        get complex trace history for all sweeps
        type:  `numpy.ndarray`
        dtype: `c16` (complex128)
        """
        # make this trace the active trace
        self.select()

        # get history for all sweeps
        index = self.channel
        vna   = self._vna
        count = vna.channel(index).sweep_count
        scpi  = f'CALC{index}:DATA:NSW:FIRS? SDAT,1,{count}'
        with PreserveDataTransferSettings(vna):
            # configure data transfer settings
            settings = vna.settings
            settings.binary_64_bit_data_format = True
            settings.little_endian = True

            # transfer data
            vna.write(scpi)
            data = vna.read_64_bit_complex_vector_block_data()

        # reshape and return
        points = len(data) // count
        return data.reshape((count, points))


    def complex_history_for_sweep(self, index):
        """
        get complex trace history for a single sweep by index

        Returns:
            `numpy.ndarray` with dtype "c16" (complex128)
        """
        # make this trace the active trace
        self.select()

        # get history at index
        vna  = self._vna
        scpi = f'CALC{self.channel}:DATA:NSW:FIRS? SDAT, {index}'
        with PreserveDataTransferSettings(vna):
            # configure data transfer settings
            settings = vna.settings
            settings.binary_64_bit_data_format = True
            settings.little_endian = True

            # transfer data
            vna.write(scpi)
            return vna.read_64_bit_complex_vector_block_data()


    def measure_formatted_data(self):
        channel = self._vna.channel(self.channel)
        is_manual = channel.manual_sweep
        channel.manual_sweep = True
        channel.start_sweep()
        self._vna.pause(2 * channel.sweep_time_ms * channel.sweep_count + 5000)
        y = self.y_formatted
        channel.manual_sweep = is_manual
        return (self.x, y)

    def measure_complex_data(self):
        channel = self._vna.channel(self.channel)
        is_manual = channel.manual_sweep
        channel.manual_sweep = True
        channel.start_sweep()
        self._vna.pause(2 * channel.sweep_time_ms * channel.sweep_count + 5000)
        y = self.y_complex
        channel.manual_sweep = is_manual
        return (self.x, y)

    def save_data(self, filename):
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        scpi = ":MMEM:STOR:TRAC '{0}', '{1}', FORM, {2}, POIN, COMM"
        scpi = scpi.format(self.name, filename, SaveDataFormat.real_imaginary)
        self._vna.write(scpi)
        self._vna.pause()
    def save_data_locally(self, filename):
        extension = ".csv"
        unique_filename = unique_alphanumeric_string() + extension
        if not filename.lower().endswith(extension):
            filename += extension
        self.save_data(unique_filename)
        self._vna.file.download_file(unique_filename, filename)
        self._vna.file.delete(unique_filename)

    def save_complex_data(self, filename, format = SaveDataFormat.real_imaginary):
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        scpi = ":MMEM:STOR:TRAC '{0}', '{1}', UNF, {2}, POIN, COMM"
        scpi = scpi.format(self.name, filename, format)
        self._vna.write(scpi)
        self._vna.pause()
    def save_complex_data_locally(self, filename, format = SaveDataFormat.real_imaginary):
        extension = ".csv"
        unique_filename = unique_alphanumeric_string() + extension
        if not filename.lower().endswith(extension):
            filename += extension
        self.save_complex_data(unique_filename, format)
        self._vna.file.download_file(unique_filename, filename)
        self._vna.file.delete(unique_filename)

    def save_complex_history_locally(self, filename):
        history = self.complex_history
        file    = Path(filename).with_suffix('.csv')
        with file.open('w') as f:
            csvwriter = csv.writer(f)
            for sweep in history:
                csvwriter.writerow(sweep.view(float))


    def is_marker(self, index):
        self.select()
        scpi = ":CALC{0}:MARK{1}?"
        scpi = scpi.format(self.channel, index)
        result = self._vna.query(scpi).strip()
        return result == "1"

    def create_marker(self, index):
        scpi = ":CALC{0}:MARK{1} 1"
        scpi = scpi.format(self.channel, index)
        self.select()
        self._vna.write(scpi)

    def delete_marker(self, index):
        scpi = ":CALC{0}:MARK{1} 0"
        scpi = scpi.format(self.channel, index)
        self._vna.write(scpi)
    def delete_markers(self):
        for marker in self.markers:
            self.delete_marker(marker)

    def _markers(self):
        markers = []
        for i in range(1,11):
            if self.is_marker(i):
                markers.append(i)
        return markers
    def _set_markers(self, markers):
        old_markers = self.markers
        for marker in markers:
            if marker not in old_markers:
                self.create_marker(marker)
        for marker in old_markers:
            if marker not in markers:
                self.delete_marker(marker)
    markers = property(_markers, _set_markers)

    def marker(self, index=1):
        return Marker(self._vna, self, index)

    def _limits(self):
        return Limits(self._vna, self)
    limits = property(_limits)

    def _time_domain(self):
        return TimeDomain(self._vna, self)
    time_domain = property(_time_domain)

    def test_ports(self):
        param = self.parameter
        # parameters that refer to
        # test ports:
        if self._is_wave(param):
            return [self._parse_wave_port(param)]
        if self._is_wave_ratio(param):
            return self._parse_wave_ratio_ports(param)
        if self._is_regular_single_param(param):
            return self._parse_regular_param_ports(param)
        # parameters that use logical
        # port notation:
        ch = self._vna.channel(self.channel)
        convert = ch.to_test_ports
        if self._is_impedance(param):
            return convert(self._parse_impedance_ports(param))
        if self._is_admittance(param):
            return convert(self._parse_admittance_ports(param))
        if self._is_regular_balanced_param(param):
            return convert(self._parse_regular_param_ports(param))
        # else
        return []

    # Private static methods for parsing
    # Trace.parameter.
    # Note: Not complete, but covers the
    # most common parameter types:
    #   wave
    #   wave ratio
    #   impedance
    #   admittance
    #   regular parameter (S, Y, Z)

    # Parameter: wave
    # ex: 'A1D1SAM'
    @staticmethod
    def _is_wave(param):
        if '/' in param:
            return False
        param = param.lower()
        if 'a' in param or 'b' in param:
            return True
        # else
        return False

    @staticmethod
    def _parse_wave_port(param):
        param = param[1:-3].lower()
        param = re.split('[dg]', param)
        return int(param[0])

    # Parameter: wave ratio
    # ex: 'A1D1/B2D1SAM'
    @staticmethod
    def _is_wave_ratio(param):
        if '/' in param:
            return True
        # else
        return False

    @staticmethod
    def _parse_wave_ratio_ports(param):
        waves = param.split('/')
        port1 = Trace._parse_wave_port(waves[0] + '   ')
        port2 = Trace._parse_wave_port(waves[1])
        if port1 != port2:
            return sorted([port1, port2])
        # else
        return [port1]

    # Parameter: impedance, admittance
    # ex: 'Z-S11' or 'Y-Sdd11'
    @staticmethod
    def _is_impedance(param):
        param = param.lower()
        if param[0:2] == 'z-':
            return True
        # else
        return False

    @staticmethod
    def _is_admittance(param):
        param = param.lower()
        if param[0:2] == 'y-':
            return True
        # else
        return False

    @staticmethod
    def _parse_impedance_ports(param):
        param = param.split('-')[-1]
        return Trace._parse_regular_param_ports(param)

    @staticmethod
    def _parse_admittance_ports(param):
        return Trace._parse_impedance_ports(param)

    # Parameter: Regular
    # single-ended or balanced
    # ex: 'S11' or 'Ydd21'
    @staticmethod
    def _is_regular_param(param):
        if '/' in param:
            return False
        if '-' in param:
            return False
        param = param.lower()
        if param[0] in ('s', 'y', 'z'):
            return True
        # else
        return False

    @staticmethod
    def _is_s_param(param):
        param = param.lower()
        return Trace._is_regular_param(param) and param[0] == 's'

    @staticmethod
    def _is_y_param(param):
        return Trace._is_regular_param(param) and param[0] == 'y'

    @staticmethod
    def _is_z_param(param):
        return Trace._is_regular_param(param) and param[0] == 'z'

    @staticmethod
    def _is_regular_single_param(param):
        if not Trace._is_regular_param(param):
            return False
        param = param.lower()
        if param[1].isdigit():
            return True
        # else
        return False

    @staticmethod
    def _is_regular_balanced_param(param):
        return Trace._is_regular_param(param) and not Trace._is_regular_single_param(param)

    @staticmethod
    def _parse_regular_param_ports(param):
        digits = ''.join(c for c in param if c.isdigit())
        return Trace._parse_two_digits(digits)

    # Parse ij port notation
    # eg S12, S0102
    @staticmethod
    def _parse_two_digits(s):
        x = len(s) // 2
        port1 = int(s[0:x])
        port2 = int(s[x:])
        if port1 != port2:
            return sorted([port1, port2])
        # else
        return [port1]
