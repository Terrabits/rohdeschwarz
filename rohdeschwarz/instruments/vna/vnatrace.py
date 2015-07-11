import sys


class VnaTrace:
    def __init__(self, vna, name='Trc1'):
        self._vna = vna
        self.name = name

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
