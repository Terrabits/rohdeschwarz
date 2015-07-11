

class VnaDiagram:
    def __init__(self, vna, index=1):
        self._vna = vna
        self.index = index

    def _title(self):
        scpi = ':DISP:WIND{0}:TITL:DATA?'
        scpi = scpi.format(self.index)
        return self._vna.query(scpi).strip().strip("'")

    def _set_title(self, title):
        scpi = ":DISP:WIND{0}:TITL:DATA '{1}'"
        scpi = scpi.format(self.index, title)
        self._vna.write(scpi)

    title = property(_title, _set_title)

    def _traces(self):
        scpi = ':DISP:WIND{0}:TRAC:CAT?'
        scpi = scpi.format(self.index)
        result = self._vna.query(scpi).strip().strip("'")
        result = result.split(',')
        return result[1::2]

    def _set_traces(self, traces):
        _traces = self._traces()
        scpi = ":DISP:WIND{0}:TRAC:EFE '{1}'"
        for t in traces:
            if not t in _traces:
                self._vna.write(scpi.format(self.index, t))
        for t in _traces:
            if not t in traces:
                self._vna.delete_trace(t)

    traces = property(_traces, _set_traces)
