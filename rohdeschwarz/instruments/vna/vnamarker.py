

class VnaMarker(object):
    def __init__(self, vna, trace, index=1):
        self._vna = vna
        self._trace = trace
        self._index = index

    def _name(self):
        scpi = ":CALC{0}:MARK{1}:NAME?"
        scpi = scpi.format(self._trace.channel, self._index)
        self._trace.select()
        return self._vna.query(scpi).strip().strip("'")
    def _set_name(self, name):
        scpi = ":CALC{0}:MARK{1}:NAME '{2}'"
        scpi = scpi.format(self._trace.channel, self._index, name)
        self._trace.select()
        self._vna.write(scpi)
    name = property(_name, _set_name)

    def _x(self):
        scpi = ":CALC{0}:MARK{1}:X?"
        scpi = scpi.format(self._trace.channel, self._index)
        self._trace.select()
        value = self._vna.query(scpi).strip()
        return float(value)
    def _set_x(self,value):
        scpi = ":CALC{0}:MARK{1}:X {2}"
        scpi = scpi.format(self._trace.channel, self._index, value)
        self._trace.select()
        self._vna.write(scpi)
    x = property(_x, _set_x)

    def _y(self):
        scpi = ":CALC{0}:MARK{1}:Y?"
        scpi = scpi.format(self._trace.channel, self._index)
        self._trace.select()
        value = self._vna.query(scpi).strip()
        return float(value)
    #   _set_y(self): ?
    y = property(_y)

    def find_max(self):
        scpi = ":CALC{0}:MARK{1}:FUNC:EXEC MAX"
        scpi = scpi.format(self._trace.channel, self._index)
        self._trace.select()
        self._vna.write(scpi)
    def find_min(self):
        scpi = ":CALC{0}:MARK{1}:FUNC:EXEC MIN"
        scpi = scpi.format(self._trace.channel, self._index)
        self._trace.select()
        self._vna.write(scpi)
    def _set_find_value(self, value):
        scpi = "CALC{0}:MARK{1}:TARG {2}"
        scpi = scpi.format(self._trace.channel, self._index, value)
        self._trace.select()
        self._vna.write(scpi)
    def find(self, value):
        self._set_find_value(value)
        scpi = ":CALC{0}:MARK{1}:FUNC:EXEC TARG"
        scpi = scpi.format(self._trace.channel, self._index)
        self._trace.select()
        self._vna.write(scpi)

