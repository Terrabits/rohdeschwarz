import pathlib
from enum import Enum
from rohdeschwarz.general import SiPrefix
from rohdeschwarz.general import unique_alphanumeric_string
from rohdeschwarz.instruments.genericinstrument import GenericInstrument
from rohdeschwarz.instruments.vna.vnachannel import VnaChannel
from rohdeschwarz.instruments.vna.vnadiagram import VnaDiagram
from rohdeschwarz.instruments.vna.vnatrace import VnaTrace
from rohdeschwarz.instruments.vna.vnaproperties import VnaProperties
from rohdeschwarz.instruments.vna.vnasettings import VnaSettings
from rohdeschwarz.instruments.vna.vnafilesystem import VnaFileSystem
from rohdeschwarz.instruments.vna.vnafilesystem import Directory


class ImageFormat(Enum):
    bmp = 'BMP'
    png = 'PNG'
    jpg = 'JPG'
    pdf = 'PDF'
    svg = 'SVG'
    def __str__(self):
        return self.value


class Vna(GenericInstrument):
    def __init__(self):
        GenericInstrument.__init__(self)
        self.properties = VnaProperties(self)
        self.settings = VnaSettings(self)
        self.file = VnaFileSystem(self)

    def print_info(self):
        _log = self.log
        self.log = None
        _log.write('VNA INSTRUMENT INFO\n')
        if self.connected() and self.properties.is_known_model():
            _log.write('Connection:       {0}\n'.format(self.connection_method))
            _log.write('Address:          {0}\n'.format(self.address))
            _log.write('Make:             Rohde & Schwarz\n')
            _log.write('Model:            {0}\n'.format(self.properties.model))
            _log.write('Serial No:        {0}\n'.format(self.properties.serial_number))
            _log.write('Firmware Version: {0}\n'.format(self.properties.firmware_version))
            value, prefix = SiPrefix.convert(self.properties.minimum_frequency_Hz)
            _log.write('Min Frequency:    {0} {1}Hz\n'.format(value, prefix))
            value, prefix = SiPrefix.convert(self.properties.maximum_frequency_Hz)
            _log.write('Max Frequency:    {0} {1}Hz\n'.format(value, prefix))
            _log.write('Number of Ports:  {0}\n'.format(self.properties.physical_ports))
            options = self.properties.options_list
            if options:
                _log.write('Options:          ')
                _log.write('\n                  '.join(options))
                _log.write('\n')
        elif self.connected():
            _log.write('Make: Unknown\n')
            _log.write('*IDN?\n  {0}\n'.format(self.id_string()))
        else:
            _log.write('Instrument not found!\n')
            _log.write('Connection:       {0}\n'.format(self.connection_method))
            _log.write('Address:          {0}\n'.format(self.address))
        _log.write('\n\n')
        self.log = _log

    def is_error(self):
        return bool(self._errors())

    def next_error(self):
        code = 0;
        message = '';
        result = self.query(':SYST:ERR?').strip()
        comma_index = result.find(',')
        code = int(result[:comma_index])
        message = result[comma_index+2:-1]
        if (code != 0):
            return(code, message)
        else:
            return None

    def _errors(self):
        errors = []
        error = self.next_error()
        while error:
            errors.append(error)
            error = self.next_error()
        return errors

    errors = property(_errors)


    ### Channels
    def is_channel(self, index):
        return index in self._channels()

    def _channels(self):
        result = self.query(':CONF:CHAN:CAT?')
        result = result.strip().strip("'")
        if len(result) == 0:
            return []
        result = result.split(",")
        result = result[::2]
        return list(map(int, result))
    def _set_channels(self, channels):
        _allChannels = self._channels()
        for c in channels:
            if c not in _allChannels:
                self.create_channel(c)
        for c in _allChannels:
            if c not in channels:
                self.delete_channel(c)
    channels = property(_channels, _set_channels)

    def create_channel(self, index=None):
        if not index:
            _channels = self._channels()
            if len(_channels) == 0:
                index = 1
            else:
                index = _channels[-1] + 1
        self.write(':CONF:CHAN{0} 1'.format(index))
        return index

    def copy_channel(self, original_index, new_index=None):
        self.channel(original_index).select()
        if not new_index:
            return create_channel()
        else:
            create_channel(new_index)

    def delete_channel(self, index):
        self.write(':CONF:CHAN{0} 0'.format(index))

    def delete_channels(self, indexes):
        for i in indexes:
            self.delete_channel(i)

    def channel(self, index=1):
        return VnaChannel(self, index)


    ### Traces
    def is_trace(self, name):
        return name in self._traces()

    def _traces(self):
        result = self.query(':CONF:TRAC:CAT?').strip().strip("'")
        if len(result) == 0:
            return []
        result = result.split(",")
        return result[1::2]
    def _set_traces(self, traces):
        _allTraces = self._traces()
        for t in traces:
            if t not in _allTraces:
                self.create_trace(name=t)
        for t in _allTraces:
            if t not in traces:
                self.delete_trace(name=t)
    traces = property(_traces, _set_traces)

    def create_trace(self, name=None, channel=1, parameter = 'S11'):
        if not name:
            traces = self.traces
            name = 'Trc1'
            i = 2
            while name in traces:
                name = 'Trc{0}'.format(i)
                i += 1
            scpi = ":CALC{0}:PAR:SDEF '{1}', '{2}'"
            scpi = scpi.format(channel, name, parameter) # Fix
            self.write(scpi)
            return name
        else:
            scpi = ":CALC{0}:PAR:SDEF '{1}', '{2}'"
            scpi = scpi.format(channel, name, parameter) # Fix
            self.write(scpi)

    def delete_trace(self, name):
        _channel = 1 # Fix
        scpi = ":CALC{0}:PAR:DEL '{1}'"
        scpi = scpi.format(_channel, name)
        self.write(scpi)

    def delete_traces(self):
        for t in self._traces():
            self.delete_trace(t)

    def trace(self, name='Trc1'):
        return VnaTrace(self, name)

    ### Diagrams
    def is_diagram(self, index):
        return index in self._diagrams()

    def _diagrams(self):
        result = self.query(':DISP:CAT?').strip().strip("'")
        if len(result) == 0:
            return []
        result = result.split(',')
        result = result[::2]
        return list(map(int, result))

    def _set_diagrams(self, diagrams):
        _allDiagrams = self._diagrams()
        while len(diagrams) > len(_allDiagrams):
            _allDiagrams.append(self.create_diagram())
        while len(diagrams) < len(_allDiagrams):
            self.delete_diagram(_allDiagrams[-1])
            _allDiagrams.pop(-1)

    diagrams = property(_diagrams, _set_diagrams)

    def create_diagram(self, index=None):
        if not index:
            _diagrams = self._diagrams()
            if len(_diagrams) == 0:
                index = 1
            else:
                index = _diagrams[-1] + 1
        self.write(':DISP:WIND{0}:STAT 1'.format(index))
        return index

    def delete_diagram(self, index):
        self.write(':DISP:WIND{0}:STAT 0'.format(index))

    def delete_diagrams(self):
        _diagrams = self._diagrams()
        while len(_diagrams) > 1:
            self.delete_diagram(_diagrams[-1])
            _diagrams = self._diagrams()

    def diagram(self, index=1):
        return VnaDiagram(self, index)


    ### Sets
    def create_set(self, name=None):
        if name:
            scpi = ":MEM:DEF '{0}'"
            scpi = scpi.format(name)
            self.write(scpi)
        else:
            sets = self.sets
            name = 'Set1'
            i = 2
            while name in sets:
                name = "Set{0}".format(i)
                i += 1
            scpi = ":MEM:DEF '{0}'"
            scpi = scpi.format(name)
            self.write(scpi)
            return name

    def open_set(self, name):
        if self.properties.is_zvx() and not name.lower().endswith('.zvx'):
            name += '.zvx'
        elif self.properties.is_znx() and not name.lower().endswith('.znx'):
            name += '.znx'
        current_dir = ''
        if str(pathlib.PureWindowsPath(name).parent) == '.':
            current_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)
        scpi = ":MMEM:LOAD:STAT 1,'{0}'"
        scpi = scpi.format(name)
        self.write(scpi)
        if current_dir:
            self.file.cd(current_dir)

    def _sets(self):
        result = self.query(":MEM:CAT?")
        result = result.strip().replace("'","")
        if not result:
            return []
        result = result.split(',')
        return result
    sets = property(_sets)

    def _set_active_set(self, name):
        scpi = ":MEM:SEL '{0}'"
        scpi = scpi.format(name)
        self.write(scpi)
    def _active_set(self):
        sets = self.sets
        if len(sets) == 0:
            return None
        if len(sets) == 1:
            return sets[0]

        # create unique trace name
        unique_trace_name = 'Trc' + unique_alphanumeric_string()
        self.create_trace(unique_trace_name, self.channels[0])
        for set in sets:
            self.active_set = set
            if unique_trace_name in self.traces:
                self.delete_trace(unique_trace_name)
                return set
        return None
    active_set = property(_active_set, _set_active_set)

    def save_active_set(self, path):
        extension = None
        if self.properties.is_zvx():
            extension = ".zvx"
        elif self.properties.is_znx():
            extension = ".znx"

        if not path.lower().endswith(extension):
            path += extension

        current_dir = None
        if str(pathlib.PureWindowsPath(path).parent) ==  '.':
            current_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)
        scpi = ":MMEM:STOR:STAT 1,'{0}'"
        scpi = scpi.format(path)
        self.write(scpi)
        self.pause()
        if current_dir:
            self.file.cd(current_dir)
    def save_active_set_locally(self, filename):
        extension = None
        if self.properties.is_zvx():
            extension = ".zvx"
        elif self.properties.is_znx():
            extension = ".znx"

        unique_filename = unique_alphanumeric_string() + extension
        if not filename.lower().endswith(extension):
            filename += extension

        self.save_active_set(unique_filename)
        current_directory = self.file.directory()
        self.file.cd(Directory.recall_sets)
        self.file.download_file(unique_filename, filename)
        self.file.delete(unique_filename)
        self.file.cd(current_directory)

    def close_set(self, name):
        scpi = ":MEM:DEL '{0}'"
        scpi = scpi.format(name)
        self.write(scpi)

    def close_sets(self):
        sets = self.sets
        for set in sets:
            self.close_set(set)

    def delete_set(self, name):
        if self.properties.is_zvx() and not name.lower().endswith('.zvx'):
            name += '.zvx'
        elif self.properties.is_znx() and not name.lower().endswith('.znx'):
            name += '.znx'
        current_dir = ''
        if str(pathlib.PureWindowsPath(name).parent) ==  '.':
            current_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)
        self.file.delete(name)
        if current_dir:
            self.file.cd(current_dir)

    ### General
    def _sweep_time_ms(self):
        sweep_time_ms = 0
        channels = self.channels
        for i in channels:
            sweep_time_ms += self.channel(i).total_sweep_time_ms
        return sweep_time_ms
    sweep_time_ms = property(_sweep_time_ms)

    def _is_manual_sweep(self):
        for c in self.channels:
            if not self.channel(c).manual_sweep:
                return False
        return True
    def _set_manual_sweep(self, value):
        for c in self.channels:
            self.channel(c).manual_sweep = value
    manual_sweep = property(_is_manual_sweep, _set_manual_sweep)

    def _is_continuous_sweep(self):
        for c in self.channels:
            if not self.channel(c).continuous_sweep:
                return False
        return True
    def _set_continuous_sweep(self, value):
        for c in self.channels:
            self.channel(c).continuous_sweep = value
    continuous_sweep = property(_is_continuous_sweep, _set_continuous_sweep)


    def start_sweeps(self):
        self.write(":INIT:SCOP ALL")
        self.write(":INIT")

    def _test_ports(self):
        if self.properties.is_zvx():
            return self.properties.physical_ports
        else:
            scpi = ':INST:TPORT:COUN?'
            result = self.query(scpi)
            return int(result.strip())
    test_ports = property(_test_ports)

    def _passed(self):
        scpi = ":CALC:CLIM:FAIL?"
        return self.query(scpi).strip() == "0"
    passed = property(_passed)

    def save_screenshot(self, filename, image_format='JPG'):
        extension = ".{0}".format(image_format).lower()
        if not filename.lower().endswith(extension):
            filename += extension
        scpi = ":MMEM:NAME '{0}'"
        scpi = scpi.format(filename)
        self.write(scpi)
        scpi = ":HCOP:DEV:LANG {0}"
        scpi = scpi.format(image_format)
        self.write(scpi)
        self.write(":HCOP:PAGE:WIND ALL")
        self.write("HCOP:DEST 'MMEM'")
        self.write(":HCOP")
        self.pause(5000)
        return self.file.is_file(filename)
    def save_screenshot_locally(self, filename, image_format='JPG'):
        extension = "." + str(image_format).lower()
        unique_filename = unique_alphanumeric_string() + extension
        if not filename.lower().endswith(extension):
            filename += extension
        if self.save_screenshot(unique_filename, image_format):
            self.file.download_file(unique_filename, filename)
            self.file.delete(unique_filename)
            return True
        else:
            return False
