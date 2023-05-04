from   .trigger             import Trigger
from   enum                 import Enum
import numpy
from   rohdeschwarz.general import SiPrefix
from   rohdeschwarz.general import unique_alphanumeric_string
from   rohdeschwarz.general import Units
from   rohdeschwarz.general import number_of_thrus


class SweepType(Enum):
    linear    = 'LIN'
    log       = 'LOG'
    segmented = 'SEGM'
    power     = 'POW'
    cw        = 'CW'
    time      = 'POIN'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if type(other) == SweepType:
            return self.value == other.value
        else:
            return self.value == other


class TouchstoneFormat(Enum):
    db_degrees = 'LOGP'
    magnitude_degrees = 'LINP'
    real_imaginary = 'COMP'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, TouchstoneFormat):
            return self.value == other.value
        else:
            return self.value == other


class Channel(object):
    def __init__(self, vna, index):
        super(Channel, self).__init__()
        self._vna = vna
        self.index = index

    def _name(self):
        scpi = ':CONF:CHAN{0}:NAME?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi)
        return result.strip().strip("'")

    def _set_name(self, name):
        scpi = ":CONF:CHAN{0}:NAME '{1}'"
        scpi = scpi.format(self.index, name)
        self._vna.write(scpi)
    name = property(_name, _set_name)

    def select(self):
        # same command as create channel
        self._vna.create_channel(self.index)

    # diagrams property?

    def _traces(self):
        scpi = "CALC{0}:PAR:CAT?"
        scpi = scpi.format(self.index)
        response = self._vna.query(scpi)
        traces   = response.strip("'").strip().split(",")[::2]
        return list(filter(None, traces))

    traces = property(_traces)

    def auto_calibrate(self, ports, characterization=''):
        scpi = ""
        if type(ports) == dict:
            def format_str(port_items):
                return "{!r},{!r}".format(*port_items)
            port_strings = [format_str(items) for items in ports.items()]
            ports_string = ",".join(port_strings)
            scpi = ":SENS{0}:CORR:COLL:AUTO:PORT '{1}',{2}"
            scpi = scpi.format(self.index, characterization, ports_string)
        else:
            scpi = ":SENS{0}:CORR:COLL:AUTO '{1}',{2}"
            ports_string = ",".join(map(str, ports))
            scpi = scpi.format(self.index, characterization, ports_string)
        port_count = len(ports)
        number_of_sweeps = 3 * port_count + number_of_thrus(port_count)
        one_sweep_ms     = 10 * self.total_sweep_time_ms + 10000
        timeout_ms = number_of_sweeps * one_sweep_ms + 5000
        self._vna.write(scpi)
        self._vna.pause(timeout_ms)

    def source_power_cal(self, port, sweeps=10, tolerance_dB=0.1):
        # sweeps
        scpi = 'SOUR{0}:POW{1}:CORR:NRE {2}'
        scpi = scpi.format(self.index, port, sweeps)
        self._vna.write(scpi)
        # tolerance
        scpi = 'SOUR{0}:POW{1}:CORR:NTOL {2}'
        scpi = scpi.format(self.index, port, tolerance_dB)
        self._vna.write(scpi)
        if self._vna.properties.is_zvx():
            # Calibrate reference receiver (a<port>-wave)
            # along with source
            self._vna.write('SOUR:POW:CORR:COLL:RREC 1')
        # Perform power cal
        scpi = 'SOUR{0}:POW:CORR:ACQ PORT,{1}'
        scpi = scpi.format(self.index, port)
        self._vna.write(scpi)
        # Source power cal can take a long time...
        # *OPC? for up to 10 mins
        ten_mins = 10 * 60 * 1000
        self._vna.pause(timeout_ms=ten_mins)

    def receiver_power_cal(self, receiver, source):
        scpi = 'SENS{0}:CORR:POW:ACQ BWAV,{1},PORT,{2}'
        scpi = scpi.format(self.index, receiver, source)
        self._vna.write(scpi)
        # Receiver power cal can take a long time...
        # *OPC? for up to 10 mins
        ten_mins = 10 * 60 * 1000
        self._vna.pause(timeout_ms=ten_mins)

    def start_sweep(self):
        scpi = ':INIT{0}'.format(self.index)
        self._vna.write(scpi)

    def sweep(self):
        self.manual_sweep = True
        timeout_ms = 2 * self.total_sweep_time_ms + 5000
        self.start_sweep()
        self._vna.pause(timeout_ms)

    def _sweep_count(self):
        scpi = ':SENS{0}:SWE:COUN?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return int(result)

    def _set_sweep_count(self, count):
        if not count or count < 0:
            raise ValueError(0, 'sweep_count must be of type int and >= 1')
        scpi = ':SENS{0}:SWE:COUN {1}'
        scpi = scpi.format(self.index, count)
        self._vna.write(scpi)
    sweep_count = property(_sweep_count, _set_sweep_count)


    # completed sweeps

    def _completed_sweeps(self):
        """
        number of completed sweeps
        type:   int
        access: read-only
        """
        scpi   = f':CALC{self.index}:DATA:NSW:COUN?'
        result = self._vna.query(scpi)
        return int(result)


    completed_sweeps = property(_completed_sweeps)


    # Define User Port, Pin 4: `UC_BUSY`

    @property
    def user_busy_signal(self):
        """User Port pin 4 `UC_BUSY` signal definition

        Note: this property is ZVX Only!

        """
        scpi = f'OUTP{self.index}:UPOR:BUSY:LINK?'
        return self._vna.query(scpi).strip()


    @user_busy_signal.setter
    def user_busy_signal(self, value):
        scpi = f'OUTP{self.index}:UPOR:BUSY:LINK {value}'
        self._vna.write(scpi)


    def _is_averaging(self):
        scpi = ":SENS{0}:AVER?"
        scpi = scpi.format(self.index)
        return self._vna.query(scpi).strip() == "1"

    def _averaging_on(self):
        scpi = ":SENS{0}:AVER 1"
        scpi = scpi.format(self.index)
        self._vna.write(scpi)

    def _averaging_off(self):
        scpi = ":SENS{0}:AVER 0"
        scpi = scpi.format(self.index)
        self._vna.write(scpi)

    def _averages(self):
        if not self._is_averaging():
            return None
        else:
            scpi = ":SENS{0}:AVER:COUN?"
            scpi = scpi.format(self.index)
            result = self._vna.query(scpi).strip()
            return int(result)

    def _set_averages(self, count):
        if not count:
            self._averaging_off()
        else:
            scpi = ":SENS{0}:AVER:COUN {1}"
            scpi = scpi.format(self.index, count)
            self._vna.write(scpi)
            self._averaging_on()

    averages = property(_averages, _set_averages)


    # sweep control

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


    # trigger settings

    @property
    def trigger(self):
        """trigger settings object"""
        return Trigger(self._vna, self.index)


    def is_frequency_sweep(self):
        sweep_type = self.sweep_type
        if sweep_type == SweepType.linear:
            return True
        if sweep_type == SweepType.log:
            return True
        if sweep_type == SweepType.segmented:
            return True
        # Else:
        return False

    def is_power_sweep(self):
        return self.sweep_type == SweepType.power

    def is_time_sweep(self):
        sweep_type = self.sweep_type
        if sweep_type == SweepType.time:
            return True
        if sweep_type == SweepType.cw:
            return True
        # else
        return False

    def _sweep_type(self):
        scpi = ':SENS{0}:SWE:TYPE?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return SweepType(result)

    def _set_sweep_type(self, value):
        scpi = ':SENS{0}:SWE:TYPE {1}'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)
    sweep_type = property(_sweep_type, _set_sweep_type)

    def x_units(self):
        if self.is_power_sweep():
            return Units.dBm
        if self.is_time_sweep():
            return Units.seconds
        # else
        return Units.Hz

    # Linear, Log frequency sweeps:
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

    def _points(self):
        scpi = ':SENS{0}:SWE:POIN?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip()
        return int(result)

    def _set_points(self, value):
        scpi = ':SENS{0}:SWE:POIN {1}'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)
    points = property(_points, _set_points)

    def _frequencies(self):
        self._vna.settings.binary_64_bit_data_format = True
        scpi = ':CALC{0}:DATA:STIM?'
        scpi = scpi.format(self.index)
        self._vna.write(scpi)
        result = self._vna.read_64_bit_vector_block_data()
        self._vna.settings.ascii_data_format = True
        return result

    def _set_frequencies(self, x, prefix=SiPrefix.none):
        if isinstance(x, (tuple, list, set)) and len(x) == 2:
            prefix = x[-1]
            x      = x[0]
        prefix = str(prefix)
        # Delete segments
        self._vna.write(":SENS{0}:SEGM:DEL:ALL".format(self.index))
        for i in range(0, len(x)):
            segment = ":SENS{0}:SEGM{1}:"
            segment = segment.format(self.index, i + 1)
            # Create segment i
            self._vna.write(segment + "ADD")
            # Set segment[i].points = 1
            self._vna.write(segment + "SWE:POIN 1")
            # Set (stop) frequency
            set_stop_freq = "FREQ:STOP {0}{1}"
            set_stop_freq = set_stop_freq.format(x[i], prefix)
            self._vna.write(segment + set_stop_freq)
        self.sweep_type = SweepType.segmented
    frequencies_Hz = property(_frequencies, _set_frequencies)

    def _power(self):
        scpi = ':SOUR{0}:POW?'.format(self.index)
        result = self._vna.query(scpi).strip()
        return float(result)

    def _set_power(self, value):
        scpi = ':SOUR{0}:POW {1} dBm'
        scpi = scpi.format(self.index, value)
        self._vna.write(scpi)
    power_dBm = property(_power, _set_power)

    # Power Sweep
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

    def _powers_dBm(self):
        self._vna.settings.binary_64_bit_data_format = True
        scpi = ':CALC{0}:DATA:STIM?'
        scpi = scpi.format(self.index)
        self._vna.write(scpi)
        result = self._vna.read_64_bit_vector_block_data()
        self._vna.settings.ascii_data_format = True
        return result
    powers_dBm = property(_powers_dBm)

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

    # All sweep types
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
        scpi = ""
        if self.sweep_type == SweepType.segmented:
            scpi = ":SENS{0}:SEGM:SWE:TIME:SUM?"
        else:
            scpi = ':SENS{0}:SWE:TIME?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip()
        return 1000.0 * float(result)

    def _set_sweep_time(self, time_ms):
        if self.sweep_type == SweepType.segmented:
            raise ValueError('Cannot set sweep time of whole segmented sweep.')
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

    def _total_sweep_time_ms(self):
        return self.sweep_count * self.sweep_time_ms
    total_sweep_time_ms = property(_total_sweep_time_ms)

    def _cal_group(self):
        scpi = ":MMEM:LOAD:CORR? {0}"
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip()
        result = result.replace("'", "")
        if not result:
            return None
        else:
            if result.lower().endswith(".cal"):
                result = result[:-4]
            return result

    def _set_cal_group(self, name):
        if not name:
            scpi = ":MMEM:LOAD:CORR:RES {0}"
            scpi = scpi.format(self.index)
            self._vna.write(scpi)
        else:
            if not name.lower().endswith('.cal'):
                name += '.cal'
            scpi = ":MMEM:LOAD:CORR {0},'{1}'"
            scpi = scpi.format(self.index, name)
            self._vna.write(scpi)
    cal_group = property(_cal_group, _set_cal_group)

    def dissolve_cal_group_link(self):
        scpi = 'MMEM:LOAD:CORR:RES {0}'
        self._vna.write(scpi.format(self.index))

    def save_cal(self, name):
        if not name.lower().endswith(".cal"):
            name += ".cal"
        scpi = ":MMEM:STOR:CORR {0},'{1}'"
        scpi = scpi.format(self.index, name)
        self._vna.write(scpi)

    def to_test_ports(self, logical_ports):
        if type(logical_ports) == int:
            scpi = ":SOUR{0}:LPOR{1}?"
            scpi = scpi.format(self.index, logical_ports)
            result = self._vna.query(scpi).strip().split(",")
            return [int(i) for i in result]
        if type(logical_ports) == list:
            result = []
            for port in logical_ports:
                result += self.to_test_ports(port)
            result.sort()
            return result
        raise TypeError("logical_ports must be int or list[int]")

    def test_to_logical_port_map(self):
        result = {}
        for i in self.logical_ports():
            test_ports = self.to_test_ports(i)
            for test_port in test_ports:
                result[test_port] = i
        return result

    def is_balanced_port(self, logical_port):
        return len(self.to_test_ports(logical_port)) == 2

    def logical_ports(self):
        scpi   = "SOUR{0}:GRO:COUN?"
        scpi   = scpi.format(self.index)
        groups = int(self._vna.query(scpi).strip())

        result  = []
        for i in range(1, groups + 1):
            scpi  = "SOUR{0}:GRO{1}:PORT?"
            scpi  = scpi.format(self.index, i)
            ports = self._vna.query(scpi)
            ports = ports.strip().split(",")
            ports = [int(i) for i in ports]
            result += ports
        return result

    def to_logical_port(self, test_port):
        port_map = self.test_to_logical_port_map()
        return port_map[test_port]

    def to_logical_ports(self, test_ports):
        result = []
        port_map = self.test_to_logical_port_map()
        for test_port in test_ports:
            logical_port = port_map[test_port]
            if logical_port not in result:
                result.append(logical_port)
        result.sort()
        return result

    def _s_parameter_group(self):
        scpi = ':CALC{0}:PAR:DEF:SGR?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip()
        if result.upper() == "NONE":
            return []
        else:
            result = result.split(',')
            return [int(x) for x in result]

    def _set_s_parameter_group(self, ports):
        if not ports or len(ports) == 0:
            scpi = ':CALC{0}:PAR:DEL:SGR'
            scpi = scpi.format(self.index)
            self._vna.write(scpi)
        else:
            scpi = ':CALC{0}:PAR:DEF:SGR {1}'
            scpi = scpi.format(self.index, ",".join(map(str, ports)))
            self._vna.write(scpi)
    s_parameter_group = property(_s_parameter_group, _set_s_parameter_group)

    def read_s_parameter_group(self):
        ports = len(self.s_parameter_group)
        is_manual_sweep = self.manual_sweep
        self.sweep()
        scpi = ':CALC{0}:DATA:SGR? SDAT'
        scpi = scpi.format(self.index)
        self._vna.settings.binary_64_bit_data_format = True
        self._vna.write(scpi)
        result = self._vna.read_64_bit_complex_vector_block_data()
        self.manual_sweep = is_manual_sweep
        self._vna.settings.ascii_data_format = True
        points = len(result) // (ports**2)
        return numpy.reshape(result, (points, ports, ports))

    def measure(self, test_ports):
        old_ports = self.s_parameter_group
        self.s_parameter_group = self.to_logical_ports(test_ports)
        result = self.read_s_parameter_group()
        self.s_parameter_group = old_ports
        return result

    def save_measurement(self, filename, test_ports, data_format='COMP'):
        old_ports = self.s_parameter_group
        is_manual_sweep = self.manual_sweep
        file_extension = '.s{0}p'.format(len(test_ports))
        if not filename.lower().endswith(file_extension):
            filename += file_extension
        self.s_parameter_group = self.to_logical_ports(test_ports)
        self.sweep()
        ports_string = ",".join(map(str, test_ports))
        if self._vna.properties.is_zvx():
            scpi = ":MMEM:STOR:TRAC:PORT:INC {0},'{1}',{2},{3}"
        else:
            scpi = ":MMEM:STOR:TRAC:PORT {0},'{1}',{2},{3}"
        scpi = scpi.format(self.index,
                           filename,
                           str(data_format),
                           ports_string)
        self._vna.write(scpi)
        self._vna.pause(5000)
        self.s_parameter_group = old_ports
        self.manual_sweep = is_manual_sweep
        return self._vna.file.is_file(filename)

    def save_measurement_locally(self, filename, test_ports, format='COMP'):
        extension = ".s{0}p".format(len(test_ports))
        unique_filename = unique_alphanumeric_string() + extension
        if not filename.lower().endswith(extension):
            filename += extension
        if self.save_measurement(unique_filename, test_ports, format):
            self._vna.file.download_file(unique_filename, filename)
            self._vna.file.delete(unique_filename)
            return True
        else:
            return False
