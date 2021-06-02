from .calunit    import CalUnit
from .channel    import Channel
from .diagram    import Diagram
from .trace      import Trace
from .properties import Properties
from .settings   import Settings
from .filesystem import FileSystem, Directory
from enum        import Enum
from io          import StringIO
from pathlib     import Path, PureWindowsPath
from rohdeschwarz.enums       import SiPrefix
from rohdeschwarz.helpers     import unique_alphanumeric_string
from rohdeschwarz.instruments import Instrument


class Vna(Instrument):
    def __init__(self):
        Instrument.__init__(self)
        self.properties = Properties(self)
        self.settings   = Settings(self)
        self.file       = FileSystem(self)

    # log
    def print_info(self):
        self.log.pause()
        if not self.is_open or not self.properties.is_known_model():
            # not connected or not known VNA:
            # use generic print_info
            Instrument.print_info(self)
            self.log.resume()
            return

        # build info str
        info = StringIO('VNA Info\n')
        info.write(f'Connection:       {self.connection_method}\n')
        info.write(f'Address:          {self.address}\n')
        info.write( 'Make:             Rohde & Schwarz\n')
        info.write(f'Model:            {self.properties.model}\n')
        info.write(f'Serial No:        {self.properties.serial_number}\n')
        info.write(f'Firmware Version: {self.properties.firmware_version}\n')

        value, prefix = SiPrefix.convert(self.properties.minimum_frequency_Hz)
        info.write(f'Min Frequency:    {value} {prefix}Hz\n')

        value, prefix = SiPrefix.convert(self.properties.maximum_frequency_Hz)
        info.write(f'Max Frequency:    {value} {prefix}Hz\n')

        info.write(f'Number of Ports:  {self.properties.physical_ports}\n')
        options = self.properties.options_list
        if options:
            info.write('Options:          \n')
            for option in options:
                info.write(f'                  {option}\n')
        info.write('\n')

        # print
        self.log.resume()
        self.log.print(info.getvalue())
        self.log.flush()

    # channels
    def is_channel(self, index):
        return index in self.channels()

    @property
    def channels(self):
        result = self.query(':CONF:CHAN:CAT?')
        result = result.strip().strip("'")
        if len(result) == 0:
            return []
        result = result.split(",")
        result = result[::2]
        return list(map(int, result))

    @channels.setter
    def channels(self, channels):
        _allChannels = self.channels
        for c in channels:
            if c not in _allChannels:
                self.create_channel(c)
        for c in _allChannels:
            if c not in channels:
                self.delete_channel(c)

    def create_channel(self, index=None):
        if not index:
            _channels = self.channels()
            if len(_channels) == 0:
                index = 1
            else:
                index = _channels[-1] + 1
        self.write(':CONF:CHAN{0} 1'.format(index))
        return index

    def delete_channel(self, index):
        self.write(':CONF:CHAN{0} 0'.format(index))

    def delete_channels(self):
        for c in self.channels:
            self.delete_channel(c)

    def channel(self, index=1):
        return Channel(self, index)


    # traces
    def is_trace(self, name):
        return name in self.traces()

    @property
    def traces(self):
        result = self.query(':CONF:TRAC:CAT?').strip().strip("'")
        if len(result) == 0:
            return []
        result = result.split(",")
        return result[1::2]

    @traces.setter
    def traces(self, traces):
        _allTraces = self.traces()
        for t in traces:
            if t not in _allTraces:
                self.create_trace(name=t)
        for t in _allTraces:
            if t not in traces:
                self.delete_trace(name=t)

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
        for t in self.traces():
            self.delete_trace(t)

    def trace(self, name='Trc1'):
        return Trace(self, name)

    # diagrams
    def is_diagram(self, index):
        return index in self.diagrams()

    @property
    def diagrams(self):
        result = self.query(':DISP:CAT?').strip().strip("'")
        if len(result) == 0:
            return []
        result = result.split(',')
        result = result[::2]
        return list(map(int, result))

    @diagrams.setter
    def diagrams(self, diagrams):
        _allDiagrams = self.diagrams()
        while len(diagrams) > len(_allDiagrams):
            _allDiagrams.append(self.create_diagram())
        while len(diagrams) < len(_allDiagrams):
            self.delete_diagram(_allDiagrams[-1])
            _allDiagrams.pop(-1)

    def create_diagram(self, index=None):
        if not index:
            _diagrams = self.diagrams()
            if len(_diagrams) == 0:
                index = 1
            else:
                index = _diagrams[-1] + 1
        self.write(':DISP:WIND{0}:STAT 1'.format(index))
        return index

    def delete_diagram(self, index):
        self.write(':DISP:WIND{0}:STAT 0'.format(index))

    def delete_diagrams(self):
        '''delete all diagrams except one due to firmware limitation'''
        _diagrams = self.diagrams
        while len(_diagrams) > 1:
            self.delete_diagram(_diagrams[-1])
            _diagrams = self.diagrams

    def diagram(self, index=1):
        return Diagram(self, index)


    # sets
    @property
    def sets(self):
        result = self.query(":MEM:CAT?")
        result = result.strip().replace("'","")
        if not result:
            return []
        result = result.split(',')
        return result

    def open_set(self, name):
        # filename must include suffix
        name = self._add_set_suffix(name)

        # directory
        dir    = PureWindowsPath(name).parent
        is_dir = str(dir) != '.'

        # change directory?
        restore_dir = None
        if not is_dir:
            restore_dir = self.file.directory()
            self.file.cd(Directory.recall_sets)

        # send scpi
        scpi = ":MMEM:LOAD:STAT 1,'{0}'".format(name)
        self.write(scpi)

        # restore directory?
        if restore_dir:
            self.file.cd(restore_dir)

    def close_set(self, name):
        scpi = ":MEM:DEL '{0}'".format(name)
        self.write(scpi)

    def close_sets(self):
        sets = self.sets
        for set in sets:
            self.close_set(set)

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

    def delete_set(self, name):
        # must have suffix
        name   = self._add_set_suffix(name)

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

    def open_set_locally(self, name):
        # name must include suffix
        name = self._add_set_suffix(name)

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

    # active set
    @property
    def active_set(self):
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

    @active_set.setter
    def active_set(self, name):
        scpi = ":MEM:SEL '{0}'"
        scpi = scpi.format(name)
        self.write(scpi)

    def save_active_set(self, path):
        # must include suffix
        path = self._add_set_suffix(path)

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
        filename  = self._add_set_suffix(filename)
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

    # cal groups
    def is_cal_group(self, name):
        name = name.lower()
        if name.endswith('.cal'):
            name = name[:-4]
        cal_groups = [i.lower() for i in self.cal_groups]
        return name in cal_groups

    @property
    def cal_groups(self):
        current_dir = self.file.directory()
        self.file.cd(Directory.cal_groups)
        cal_groups = self.file.files()
        def is_cal(filename):
            return filename.lower().endswith('.cal')
        cal_groups = list(filter(is_cal, cal_groups))
        cal_groups = [name[:-4] for name in cal_groups]
        self.file.cd(current_dir)
        return cal_groups

    # cal units
    @property
    def cal_units(self):
        results = self.query(':SYST:COMM:RDEV:AKAL:ADDR:ALL?')
        results = results.strip().strip("'")
        if not results:
            return []
        else:
            return [unit.strip("'") for unit in results.split(',')]

    def cal_unit(self, id=None):
        return CalUnit(self, id)

    # power sensors
    @property
    def power_sensors(self):
        scpi = 'SYST:COMM:RDEV:PMET:CAT?'
        sensors = self.query(scpi)
        sensors = sensors.strip().split(',')
        return [int(i) for i in sensors if i]

    # sweep
    @property
    def sweep_time_ms(self):
        sweep_time_ms = 0
        channels = self.channels
        for i in channels:
            sweep_time_ms += self.channel(i).total_sweep_time_ms
        return sweep_time_ms

    @property
    def manual_sweep(self):
        for c in self.channels:
            if not self.channel(c).manual_sweep:
                return False
        return True

    @manual_sweep.setter
    def manual_sweep(self, value):
        for c in self.channels:
            self.channel(c).manual_sweep = value

    @property
    def continuous_sweep(self):
        return not self.manual_sweep
    @continuous_sweep.setter
    def continuous_sweep(self, value):
        self.manual_sweep = not value

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

    @property
    def sweep_count(self):
        indexes = self.channels
        sweep_count = self.channel(indexes.pop(0)).sweep_count
        for i in indexes:
            if self.channel(i).sweep_count != sweep_count:
                raise ValueError('channel sweep counts are not equal')
        return sweep_count

    @sweep_count.setter
    def sweep_count(self, sweep_count):
        for index in self.channels:
            self.channel(index).sweep_count = sweep_count

    # limits
    @property
    def is_limits(self):
        for i in self.traces:
            t = self.trace(i)
            if t.limits.on:
                return True
        # else
        return False

    @property
    def passed(self):
        scpi = ":CALC:CLIM:FAIL?"
        return self.query(scpi).strip() == "0"

    @property
    def failed(self):
        return not self.passed

    # screenshots
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

    # helpers
    def test_ports(self):
        if self.properties.is_zvx():
            return self.properties.physical_ports
        else:
            scpi = ':INST:TPORT:COUN?'
            result = self.query(scpi)
            return int(result.strip())

    @property
    def set_suffix(self):
        if self.properties.is_zvx():
            return '.zvx'
        if self.properties.is_znx():
            return '.znx'

        # default to znx
        return '.znx'

    def _add_set_suffix(self, name):
        path = PureWindowsPath(name.lower())
        if self.properties.is_znx():
            # znx has two set file extensions
            suffixes  = ['.znx', '.znxml']
            if path.suffix in suffixes:
                return name

        return name.with_suffix(self.set_suffix)
