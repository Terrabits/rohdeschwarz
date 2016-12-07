import sys
from enum import Enum
import numpy
from rohdeschwarz.general import unique_alphanumeric_string
from rohdeschwarz.instruments.vna.vnamarker import VnaMarker
from rohdeschwarz.instruments.vna.vnalimits import VnaLimits

class TraceFormat(Enum):
    magnitude_dB = 'MLOG'
    phase_deg = 'PHAS'
    smith_chart = 'SMIT'
    polar = 'POL'
    vswr = 'SWR'
    unwrapped_phase_deg = 'UPH'
    magnitude = 'MLIN'
    inverse_smith_chart = 'ISM'
    real = 'REAL'
    imaginary = 'IMAG'
    group_delay = 'GDEL'
    def __str__(self):
        return self.value
    def __eq__(self, other):
        if isinstance(other, TraceFormat):
            return self.value == other.value
        else:
            return self.value == other

class SaveDataFormat(Enum):
    real_imaginary = 'COMP'
    dB_degrees = 'LOGP'
    magnitude_degrees = 'LINP'
    def __str__(self):
        return self.value

class VnaTrace(object):
    def __init__(self, vna, name='Trc1'):
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
            _diagrams = self._vna.diagrams
            for d in _diagrams:
                _traces = self._vna.diagram(d).traces
                if _traces.index(self.name) != -1:
                    return d
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
        self.select()
        scpi = ':CALC{0}:FORM?'
        scpi = scpi.format(self.channel)
        result = self._vna.query(scpi).strip()
        return TraceFormat(result)
    def _set_format(self, value):
        self.select()
        scpi = ':CALC{0}:FORM {1}'
        scpi = scpi.format(self.channel, value)
        self._vna.write(scpi)
    format = property(_format, _set_format)

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
        return VnaMarker(self._vna, self, index)

    def _limits(self):
        return VnaLimits(self._vna, self)
    limits = property(_limits)
