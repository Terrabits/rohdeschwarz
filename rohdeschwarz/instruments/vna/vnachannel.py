from enum import Enum
from rohdeschwarz.general import SiPrefix

class SweepType(Enum):
    linear = 'LIN'
    log = 'LOG'
    segmented = 'SEGM'
    power = 'POW'
    cw = 'CW'
    time = 'POIN'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if type(other) == SweepType:
            return self.value == other.value
        else:
            return self.value == other


class VnaChannel:
    def __init__(self, vna, index):
        self._vna = vna
        self.index = index

    def name(self):
        scpi = ':CONF:CHAN{0}:NAME?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi)
        return result.strip().strip("'")

    def set_name(self, name):
        scpi = ":CONF:CHAN{0}:NAME '{1}'"
        scpi = scpi.format(self.index, name)
        self._vna.write(scpi)

    def select(self):
        # same command as create channel
        self._vna.create_channel(self.index)

    def diagrams(self):
        # Unfinished
        return []

    def traces(self):
        # Unfinished
        return []

    def start_sweep(self):
        scpi = ':INIT{0}'.format(self.index)
        self._vna.write(scpi)

    def _sweep_count(self):
        scpi = ':SENS{0}:SWE:COUN?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return int(result)

    def _set_sweep_count(self, count):
        scpi = ':SENS{0}:SWE:COUN {1}'
        scpi = scpi.format(self.index, count)
        self._vna.write(scpi)

    sweep_count = property(_sweep_count, _set_sweep_count)

    def _is_manual_sweep(self):
        return not self._is_continuous_sweep()

    def _set_manual_sweep(self, value):
        self._set_continuous_sweep(not value)

    manual_sweep = property(_is_manual_sweep, _set_manual_sweep)

    def _is_continuous_sweep(self):
        scpi = ':INIT{0}:CONT?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return result == '1'

    def _set_continuous_sweep(self, value):
        scpi = ':INIT{0}:CONT {1}'.format(self.index, int(value))
        self._vna.write(scpi)

    continuous_sweep = property(_is_continuous_sweep, _set_continuous_sweep)

    def _sweep_type(self):
        scpi = ':SENS{0}:SWE:TYPE?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return SweepType(result)

    def _set_sweep_type(self, value):
        scpi = ':SENS{0}:SWE:TYPE {1}'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)

    sweep_type = property(_sweep_type, _set_sweep_type)


    ### Linear, Log frequency sweeps:
    def _start_frequency(self):
        scpi = ':SENS{0}:FREQ:STAR?'
        scpi = scpi.format(self.index)
        return float(self._vna.query(scpi).strip())

    def _set_start_frequency(self, value, prefix=SiPrefix.none):
        if isinstance(value, (tuple, list, set)) and len(value) == 2:
            prefix = value[-1]
            value = value[0]
        prefix = str(prefix)
        if prefix.upper().find('HZ') == -1:
            prefix += 'Hz'
        scpi = ':SENS{0}:FREQ:STAR {1} {2}'
        scpi = scpi.format(self.index, value, prefix)
        self._vna.write(scpi)

    start_frequency_Hz = property(_start_frequency, _set_start_frequency)

    def _stop_frequency(self):
        scpi = ':SENS{0}:FREQ:STOP?'
        scpi = scpi.format(self.index)
        return float(self._vna.query(scpi).strip())

    def _set_stop_frequency(self, value, prefix=SiPrefix.none):
        if isinstance(value, (tuple, list, set)) and len(value) == 2:
            prefix = value[-1]
            value = value[0]
        prefix = str(prefix)
        if prefix.upper().find('HZ') == -1:
            prefix += 'Hz'
        scpi = ':SENS{0}:FREQ:STOP {1} {2}'
        scpi = scpi.format(self.index, value, prefix)
        self._vna.write(scpi)

    stop_frequency_Hz = property(_stop_frequency, _set_stop_frequency)

    def _frequencies(self):
        scpi = ':CALC{0}:DATA:STIM?'
        scpi = scpi.format(self.index)
        return self._vna.queryVector(scpi)

    frequencies_Hz = property(_frequencies)

    def _power(self):
        scpi = ':SOUR{0}:POW?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return float(result)

    def _set_power(self, value):
        scpi = ':SOUR{0}:POW {1} dBm'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)

    power_dBm = property(_power, _set_power)


    ### Power sweep:
    def _start_power(self):
        scpi = ':SOUR{0}:POW:STAR?'
        scpi = scpi.format(self.index)
        return float(self._vna.query(scpi).strip())

    def _set_start_power(self, value):
        scpi = ':SOUR{0}:POW:STAR {1} dBm'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)

    start_power_dBm = property(_start_power, _set_start_power)

    def _stop_power(self):
        scpi = ':SOUR{0}:POW:STOP?'
        scpi = scpi.format(self.index)
        return float(self._vna.query(scpi).strip())

    def _set_stop_power(self, value, prefix=SiPrefix.none):
        scpi = ':SOUR{0}:POW:STOP {1} dBm'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)

    stop_power_dBm = property(_stop_power, _set_stop_power)

    def _frequency(self):
        scpi = ':SOUR{0}:FREQ?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return float(result)

    def _set_frequency(self, value, prefix=SiPrefix.none):
        if isinstance(value, (tuple, list, set)) and len(value) == 2:
            prefix = value[-1]
            value = value[0]
        prefix = str(prefix)
        if prefix.upper().find('HZ') == -1:
            prefix += 'Hz'
        scpi = ':SOUR{0}:FREQ {1} {2}'
        scpi = scpi.format(self.index, value, prefix)
        self._vna.write(scpi)

    frequency_Hz = property(_frequency, _set_frequency)

    ### All sweep types
    def _if_bandwidth(self):
        scpi = 'SENS{0}:BAND?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return float(result)

    def _set_if_bandwidth(self, value, prefix=SiPrefix.none):
        if isinstance(value, (tuple, list, set)) and len(value) == 2:
            prefix = value[-1]
            value = value[0]
        prefix = str(prefix)
        if prefix.upper().find('HZ') == -1:
            prefix += 'Hz'
        scpi = 'SENS{0}:BAND {1} {2}'
        scpi = scpi.format(self.index, value, prefix)
        self._vna.write(scpi)

    if_bandwidth_Hz = property(_if_bandwidth, _set_if_bandwidth)

    def _sweep_time(self):
        scpi = ':SENS{0}:SWE:TIME?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip()
        return int(1000.0 * float(result))

    def _set_sweep_time(self, time_ms):
        scpi = ':SENS{0}:SWE:TIME {1} ms'
        scpi = scpi.format(self.index, time_ms)
        self._vna.write(scpi)

    sweep_time_ms = property(_sweep_time, _set_sweep_time)

    def _auto_sweep_time(self):
        scpi = ':SENS{0}:SWE:TIME:AUTO?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip()
        return result == "1"

    def _set_auto_sweep_time(self, value):
        scpi = ':SENS{0}:SWE:TIME:AUTO {1}'
        if value:
            scpi = scpi.format(self.index, 1)
        else:
            scpi = scpi.format(self.index, 0)
        self._vna.write(scpi)

    auto_sweep_time = property(_auto_sweep_time, _set_auto_sweep_time)


