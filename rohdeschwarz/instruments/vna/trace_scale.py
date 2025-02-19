class TraceScale(object):

    def __init__(self, vna, trace):
        super(TraceScale, self).__init__()
        self._vna  = vna
        self._trace = trace


    # scale per division

    def _scale_per_division(self):
        scpi  = 'DISP:WIND{0}:TRAC{1}:Y:PDIV?'
        scpi  = scpi.format(self._trace.diagram, self._trace.diagram_index)
        value = self._vna.query(scpi)
        return float(value)

    def _set_scale_per_division(self, value):
        scpi  = "DISP:WIND:TRAC:Y:PDIV {0},'{1}'"
        scpi  = scpi.format(value, self._trace.name)
        self._vna.write(scpi)

    scale_per_division = property(_scale_per_division, _set_scale_per_division)


    # reference value

    def _reference_value(self):
        scpi  = "DISP:WIND{0}:TRAC{1}:Y:RLEV?"
        scpi  = scpi.format(self._trace.diagram, self._trace.diagram_index)
        value = self._vna.query(scpi)
        return float(value)

    def _set_reference_value(self, value):
        scpi = "DISP:WIND:TRAC:Y:RLEV {0},'{1}'"
        scpi = scpi.format(value, self._trace.name)
        self._vna.write(scpi)

    reference_value = property(_reference_value, _set_reference_value)


    # reference position (0.0-10.0)

    def _reference_position(self):
        scpi  = 'DISP:WIND{0}:TRAC{1}:Y:RPOS?'
        scpi  = scpi.format(self._trace.diagram, self._trace.diagram_index)
        value = self._vna.query(scpi)
        return float(value) / 10.0

    def _set_reference_position(self, value):
        scpi  = "DISP:WIND:TRAC:Y:RPOS {0},'{1}'"
        scpi  = scpi.format(10.0 * value, self._trace.name)
        self._vna.write(scpi)

    reference_position = property(_reference_position, _set_reference_position)


    # maximum

    def _maximum(self):
        scpi  = 'DISP:WIND{0}:TRAC{1}:Y:TOP?'
        scpi  = scpi.format(self._trace.diagram, self._trace.diagram_index)
        value = self._vna.query(scpi)
        return float(value)

    def _set_maximum(self, value):
        scpi  = "DISP:WIND:TRAC:Y:TOP {0},'{1}'"
        scpi  = scpi.format(value, self._trace.name)
        self._vna.write(scpi)

    maximum = property(_maximum, _set_maximum)


    # minimum

    def _minimum(self):
        scpi  = 'DISP:WIND{0}:TRAC{1}:Y:BOTT?'
        scpi  = scpi.format(self._trace.diagram, self._trace.diagram_index)
        value = self._vna.query(scpi)
        return float(value)

    def _set_minimum(self, value):
        scpi  = "DISP:WIND:TRAC:Y:BOTT {0},'{1}'"
        scpi  = scpi.format(value, self._trace.name)
        self._vna.write(scpi)

    minimum = property(_minimum, _set_minimum)
