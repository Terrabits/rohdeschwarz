

class Limits(object):
    def __init__(self, vna, trace):
        self._vna = vna
        self._trace = trace

    @property
    def passed(self):
        scpi = ":CALC{0}:LIM:FAIL?"
        scpi = scpi.format(self._trace.channel)
        self._trace.select()
        return self._vna.query(scpi).strip() == "0"

    @property
    def failed(self):
        return not self.passed

    @property
    def on(self):
        scpi = ":CALC{0}:LIM:STAT?"
        scpi = scpi.format(self._trace.channel)
        self._trace.select()
        return self._vna.query(scpi).strip() == "1"

    @on.setter
    def on(self, state):
        scpi  = ":CALC{0}:LIM:STAT {1}"
        state = 1 if state else 0
        scpi  = scpi.format(self._trace.channel, state)
        self._trace.select()
        self._vna.write(scpi)

    @property
    def visible(self):
        scpi = ":CALC{0}:LIM:DISP?"
        scpi = scpi.format(self._trace.channel)
        self._trace.select()
        return self._vna.query(scpi).strip() == "1"

    @visible.setter
    def visible(self, visible):
        scpi = ":CALC{0}:LIM:DISP {1}"
        visible = 1 if visible else 0
        scpi = scpi.format(self._trace.channel, visible)
        self._trace.select()
        self._vna.write(scpi)

    def apply_file(self, filename):
        scpi = "MMEM:LOAD:LIM '{0}', '{1}'"
        scpi = scpi.format(self._trace.name, filename)
        self._vna.write(scpi)
        self.on      = True
        self.visible = True

    def upload_and_apply_file(self, filename):
        dest = '~temp.limit'
        self._vna.file.upload_file(filename, dest)
        self.apply_file(dest)
        self._vna.file.delete(dest)

    def save(self, filename):
        trace_name = self._trace.name
        scpi = "MMEM:STOR:LIM '{0}','{1}'"
        scpi = scpi.format(trace_name, filename)
        self._vna.write(scpi)

    def save_locally(self, filename):
        temp = '~temp.limit'
        self.save(temp)
        is_success = self._vna.file.download_file(temp, filename)
        self._vna.file.delete(temp)
        return is_success

    def clear(self):
        scpi = ":CALC{0}:LIM:DEL:ALL"
        scpi = scpi.format(self._trace.channel)
        self._trace.select()
        self._vna.write(scpi)
        self.on      = False
        self.visible = False
