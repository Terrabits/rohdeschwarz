

class VnaLimits(object):
    def __init__(self, vna, trace):
        self._vna = vna
        self._trace = trace

    def _passed(self):
        scpi = ":CALC{0}:LIM:FAIL?"
        scpi = scpi.format(self._trace.channel)
        self._trace.select()
        return self._vna.query(scpi).strip() == "0"
    passed = property(_passed)

    def _failed(self):
        return not self.passed
    failed = property(_failed)