from rohdeschwarz.instruments.genericinstrument import GenericInstrument
from rohdeschwarz.instruments.vna.vnachannel import VnaChannel
from rohdeschwarz.instruments.vna.vnadiagram import VnaDiagram
from rohdeschwarz.instruments.vna.vnatrace import VnaTrace
from rohdeschwarz.instruments.vna.vnaproperties import VnaProperties
from rohdeschwarz.instruments.vna.vnasettings import VnaSettings

class Vna(GenericInstrument):

    def __init__(self):
        GenericInstrument.__init__(self)
        self.properties = VnaProperties(self)
        self.settings = VnaSettings(self)

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


    ### Properties
    #set in constructor:
    #    self.properties = VnaProperties(self)


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
                self.create_trace(t)
        for t in _allTraces:
            if t not in traces:
                self.delete_trace(t)

    traces = property(_traces, _set_traces)


    def create_trace(self, name=None, channel=1):
        if not name:
            # Fix
            name = 'Trc1'
        scpi = ":CALC{0}:PAR:SDEF '{1}', '{2}'"
        scpi = scpi.format(channel, name, 'S11') # Fix
        self.write(scpi)
        return name

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

