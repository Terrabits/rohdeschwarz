from rohdeschwarz.test.mock.instruments.genericinstrument import GenericInstrument
from rohdeschwarz.test.mock.instruments.vna.calunit       import CalUnit
from rohdeschwarz.test.mock.instruments.vna.channel       import Channel
from rohdeschwarz.test.mock.instruments.vna.diagram       import Diagram
from rohdeschwarz.test.mock.instruments.vna.properties    import Properties
from rohdeschwarz.test.mock.instruments.vna.trace         import Trace
from rohdeschwarz.test.mock.instruments.vna.settings      import Settings

from rohdeschwarz.test.mock.bus                           import FifoBus

class Vna(GenericInstrument):
    def __init__(self, model='ZNBT8', ports=24):
        super(Vna, self).__init__()
        self.properties = Properties(self, model, ports)
        self.settings   = Settings(self)

        self.test_ports        = ports

        self.sets              = []
        self.active_set        = None

        self.mock_channels     = []
        self.selected_channel  = None
        self.mock_traces       = []
        self.selected_trace    = None
        self.mock_diagrams     = []
        self.selected_diagram  = None
        self.manual_sweep      = False
        self.preset()

        self.mock_cal_units    = []
        self.selected_cal_unit = None

        self.cal_groups        = []

    def read(self):
        return self.bus.read()
    def write(self, scpi):
        self.bus.write(scpi)
    def query(self, scpi):
        self.write(scpi)
        return self.read()

    def _continuous_sweep(self):
        return not self.manual_sweep
    def _set_continuous_sweep(self, value):
        self.manual_sweep = not value
    continuous_sweep = property(_continuous_sweep, _set_continuous_sweep)

    def start_sweeps(self):
        pass

    def sweep(self):
        pass

    def id_string(self):
        id = 'Rohde-Schwarz,{0}-{1}Port,{2},{3}'
        id = id.format(self.properties.model,
                       self.properties.physical_ports,
                       self.properties.serial_number,
                       self.properties.firmware_version)
        return id
    def options_string(self):
        return ",".join(self.properties.options_list)
    def preset(self):
        GenericInstrument.preset(self)
        self.sets          = ['Set1']
        self.active_set    = 'Set1'
        ch1                = Channel(self, 1)
        self.mock_channels = [ch1]
        self.select_channel(ch1)
        trc1               = Trace(self, 'Trc1', 1, 'S21')
        trc1.diagram       = 1
        self.mock_traces   = [trc1]
        self.select_trace(trc1)
        diag1              = Diagram(self, 1)
        self.mock_diagrams = [diag1]
        self.select_diagram(diag1)

    # sets
    def close_sets(self):
        self.sets.clear()
        self.active_set = None
    def open_set(self, name):
        if not name in self.sets:
            self.sets.append(name)
            self.sets.sort()
        self.active_set = name

    # channels
    def select_channel(self, i):
        i = int(i)
        if i in self.mock_channels:
            self.selected_channel = i
        else:
            self.errors.append(())
    def channel(self, index=1):
        return self.mock_channels[self.mock_channels.index(index)]
    def create_channel(self, index=None):
        if not index:
            if len(self.channels) == 0:
                index = 1
            else:
                index = self.channels[-1] + 1
        if not index in self.mock_channels:
            self.mock_channels.append(Channel(self, index))
            self.mock_channels.sort()
        return index
    def _channels(self):
        return [int(i) for i in self.mock_channels]
    def _set_channels(self, channels):
        for i in self.mock_channels:
            if not i in channels:
                self.mock_channels.pop(i)
        for i in channels:
            if not i in self.mock_channels:
                self.create_channel(int(i))
        self.mock_channels.sort()
    channels = property(_channels, _set_channels)

    # traces
    def select_trace(self, name):
        name = str(name)
        if name in self.mock_traces:
            self.selected_trace = name
    def trace(self, name='Trc1'):
        return self.mock_traces[self.mock_traces.index(name)]
    def delete_trace(self, name):
        if name in self.mock_traces:
            self.mock_traces.remove(name)
    def delete_traces(self):
        self.mock_traces.clear()
    def create_trace(self, name=None, channel=1, parameter = 'S11'):
        if not name:
            name = 'Trc{0}'
            i    = 1
            while name.format(i) in self.mock_traces:
                i += 1
            name = name.format(i)
        if not name in self.mock_traces:
            self.mock_traces.append(Trace(self, name, channel, parameter))
            self.mock_traces.sort()
        return name
    def _traces(self):
        return [str(i) for i in self.mock_traces]
    def _set_traces(self, traces):
        for i in self.mock_traces:
            if not i in traces:
                self.mock_traces.pop(i)
        for i in traces:
            if not i in self.mock_traces:
                self.create_trace(str(i))
    traces = property(_traces, _set_traces)

    # diagrams
    def select_diagram(self, diagram):
        diagram = int(diagram)
        if diagram in self.mock_diagrams:
            self.selected_diagram = diagram
    def diagram(self, index=1):
        return self.mock_diagrams[self.mock_diagrams.index(index)]
    def create_diagram(self, index=None):
        if not index:
            i = self.diagrams[-1] + 1
        if not index in self.mock_diagrams:
            self.mock_diagrams.append(Diagram(self, index))
            self.mock_diagrams.sort()
        return index
    def _diagrams(self):
        return [int(i) for i in self.mock_diagrams]
    def _set_diagrams(self, diagrams):
        for i in self.mock_diagrams:
            if not i in diagrams:
                self.mock_diagrams.pop(i)
        for i in diagrams:
            if not i in self.mock_diagrams:
                self.create_diagram(int(i))
    diagrams = property(_diagrams, _set_diagrams)

    # cal groups
    def is_cal_group(self, name):
        return name in self.cal_groups

    # cal unit
    def select_cal_unit(self, name):
        if name in self.cal_units:
            self.selected_cal_unit = self.mock_cal_units[self.cal_units.index(name)]
    def cal_unit(self, name=None):
        if not name:
            if self.selected_cal_unit:
                return self.selected_cal_unit
        else:
            return self.mock_cal_units[self.cal_units.index(name)]
    def add_cal_unit(self, name=None):
        if not name:
            name = 'CalUnit{0}'
            i = len(self.cal_units) + 1
            while name.format(i) in self.cal_units:
                i += 1
            name = name.format(i)
        if not name in self.cal_units:
            cal_unit = CalUnit(self, name)
            self.mock_cal_units.append(cal_unit)
            self.mock_cal_units.sort()
        self.select_cal_unit(name)
    def _cal_units(self):
        return [str(i) for i in self.mock_cal_units]
    cal_units = property(_cal_units)
