from pathlib import Path, PureWindowsPath
from enum    import Enum
from rohdeschwarz.general                       import SiPrefix
from rohdeschwarz.general                       import unique_alphanumeric_string
from rohdeschwarz.instruments.genericinstrument import GenericInstrument
from rohdeschwarz.instruments.vna.calunit       import CalUnit
from rohdeschwarz.instruments.vna.channel       import Channel
from rohdeschwarz.instruments.vna.diagram       import Diagram
from rohdeschwarz.instruments.vna.trace         import Trace
from rohdeschwarz.instruments.vna.properties    import Properties
from rohdeschwarz.instruments.vna.settings      import Settings
from rohdeschwarz.instruments.vna.filesystem    import FileSystem, Directory


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
        super(Vna, self).__init__()
        self.properties = Properties(self)
        self.settings = Settings(self)
        self.file = FileSystem(self)

    def __del__(self):
        if self.connected():
            self.local()
            self.close()

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
        return Channel(self, index)


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
        _channel = self.trace(name).channel
        scpi = ":CALC{0}:PAR:DEL '{1}'"
        scpi = scpi.format(_channel, name)
        self.write(scpi)

    def delete_traces(self):
        for t in self._traces():
            self.delete_trace(t)

    def trace(self, name='Trc1'):
        return Trace(self, name)

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
        return Diagram(self, index)


    ### Sets
    def __add_set_suffix(self, name):
        path = PureWindowsPath(name.lower())
        if self.properties.is_zvx():
            suffix    = '.zvx'
            is_suffix = path.suffix == suffix
            if not is_suffix:
                name += suffix
            return name
        if self.properties.is_znx():
            suffixes  = ['.znx', '.znxml']
            is_suffix = path.suffix in suffixes
            if not is_suffix:
                name += suffixes[0]
            return name
        # else unknown model, do nothing to name
        return name

    def create_set(self, name=None):
        if name:
            scpi = ":MEM:DEF '{0}'".format(name)
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
        # filename must include suffix
        name = self.__add_set_suffix(name)

        # file exists?
        restore_dir = None
        if not self.file.is_file(name):
            # try recallsets folder
            restore_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)

        scpi = ":MMEM:LOAD:STAT 1,'{0}'".format(name)
        self.write(scpi)

        # restore directory?
        if restore_dir:
            self.file.cd(restore_dir)

    def open_set_locally(self, name):
        # name must include suffix
        name = self.__add_set_suffix(name)

        # cd into RecallSets
        restore_dir = self.file.directory()
        self.file.cd(Directory.recall_sets)

        # upload set file
        filename = Path(name).name
        self.file.upload_file(name, filename)
        self.pause(10000)

        # open set
        self.open_set(filename)

        # restore dir
        self.file.cd(restore_dir)

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
        # must include suffix
        path = self.__add_set_suffix(path)

        # directory
        dir    = PureWindowsPath(path).parent
        is_dir = str(dir) != '.'

        # change directory
        restore_dir = None
        if not is_dir:
            restore_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)

        scpi = ":MMEM:STOR:STAT 1,'{0}'"
        scpi = scpi.format(path)
        self.write(scpi)
        self.pause()

        if restore_dir:
            self.file.cd(restore_dir)

    def save_active_set_locally(self, filename):
        # must include suffix
        filename  = self.__add_set_suffix(filename)
        suffix    = Path(filename).suffix

        # save on VNA in RecallSets
        temp_file = unique_alphanumeric_string() + suffix
        self.save_active_set(temp_file)

        # cd into RecallSets
        restore_dir = self.file.directory()
        self.file.cd(Directory.recall_sets)

        # download set file
        self.file.download_file(temp_file, filename)

        # delete temp file from VNA
        self.file.delete(temp_file)

        # restore dir
        self.file.cd(restore_dir)

    def close_set(self, name):
        scpi = ":MEM:DEL '{0}'".format(name)
        self.write(scpi)

    def close_sets(self):
        sets = self.sets
        for set in sets:
            self.close_set(set)

    def delete_set(self, name):
        # must have suffix
        name   = self.__add_set_suffix(name)

        # directory
        dir    = PureWindowsPath(name).parent
        is_dir = dir != '.'

        # cd into RecallSets?
        restore_dir = None
        if not is_dir:
            restore_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)

        # delete file
        self.file.delete(name)

        # restore directory?
        if restore_dir:
            self.file.cd(restore_dir)

    ### Cal groups
    def is_cal_group(self, name):
        name = name.lower()
        if name.endswith('.cal'):
            name = name[:-4]
        cal_groups = [i.lower() for i in self.cal_groups]
        return name in cal_groups

    def _cal_groups(self):
        current_dir = self.file.directory()
        self.file.cd(Directory.cal_groups)
        cal_groups = self.file.files()
        def is_cal(filename):
            return filename.lower().endswith('.cal')
        cal_groups = list(filter(is_cal, cal_groups))
        cal_groups = [name[:-4] for name in cal_groups]
        self.file.cd(current_dir)
        return cal_groups
    cal_groups = property(_cal_groups)

    # cal units
    def _cal_units(self):
        results = self.query(':SYST:COMM:RDEV:AKAL:ADDR:ALL?')
        results = results.strip().strip("'")
        if not results:
            return []
        else:
            return [unit.strip("'") for unit in results.split(',')]
    cal_units = property(_cal_units)
    def cal_unit(self, id=None):
        return CalUnit(self, id)

    # power sensors
    def _power_sensors(self):
        scpi = 'SYST:COMM:RDEV:PMET:CAT?'
        sensors = self.query(scpi)
        sensors = sensors.strip().split(',')
        return [int(i) for i in sensors if i]
    power_sensors = property(_power_sensors)

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
        if self.properties.is_zvx():
            self.write(':INIT:CONT 0')
            self.write(':INIT:SCOP ALL')
            self.write(":INIT")
            return
        # else
        self.write(':INIT:CONT:ALL 0')
        self.write(":INIT:ALL")

    def sweep(self):
        self.manual_sweep = True
        timeout_ms = 2 * self.sweep_time_ms + 5000
        self.start_sweeps()
        self.pause(timeout_ms)

    def _sweep_count(self):
        indexes = self.channels
        sweep_count = self.channel(indexes.pop(0)).sweep_count
        for i in indexes:
            if self.channel(i).sweep_count != sweep_count:
                raise ValueError('channel sweep counts are not equal')
        return sweep_count
    def _set_sweep_count(self, sweep_count):
        for index in self.channels:
            self.channel(index).sweep_count = sweep_count
    sweep_count = property(_sweep_count, _set_sweep_count)


    def _test_ports(self):
        if self.properties.is_zvx():
            return self.properties.physical_ports
        else:
            scpi = ':INST:TPORT:COUN?'
            result = self.query(scpi)
            return int(result.strip())
    test_ports = property(_test_ports)

    def is_limits(self):
        for i in self.traces:
            t = self.trace(i)
            if t.limits.on:
                return True
        # else
        return False

    def _passed(self):
        scpi = ":CALC:CLIM:FAIL?"
        return self.query(scpi).strip() == "0"
    passed = property(_passed)
    def _failed(self):
        return not self.passed
    failed = property(_failed)

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
