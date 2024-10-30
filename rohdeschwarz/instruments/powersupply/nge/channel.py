class Channel:


    # constructor
    def __init__(self, nge, index):
        self.nge = nge
        self.index = index


    # select; this becomes active channel
    def select(self):
        self.nge.write(f'INST:SEL OUTP{self.index}')


    # channel voltage
    @property
    def voltage_V(self):
        self.select()
        result = self.nge.query('MEAS:VOLT?')
        return float(result)


    # channel current
    @property
    def current_A(self):
        self.select()
        result = self.nge.query('MEAS:CURR?')
        return float(result)
