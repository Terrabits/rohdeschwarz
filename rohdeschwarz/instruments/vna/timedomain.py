
class TimeDomain(object):
    def __init__(self, vna, trace):
        self._vna = vna
        self._trace = trace

    def _on(self):
    	scpi = "CALC{0}:TRAN:TIME:STAT?"
    	scpi = scpi.format(self._trace.channel)
    	self._trace.select()
    	return self._vna.query(scpi).strip() == "1"
    def _set_on(self, is_on):
    	is_on = 1 if is_on else 0
    	scpi  = "CALC{0}:TRAN:TIME:STAT {1}"
    	scpi  = scpi.format(self._trace.channel, is_on)
    	self._trace.select()
    	self._vna.write(scpi)
    on = property(_on, _set_on)
