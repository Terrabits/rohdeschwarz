class Channel:


    # constructor
    def __init__(self, ngu, index):
        self.ngu = ngu
        self.index = index


    # select; this becomes active channel
    def select(self):
        self.ngu.write(f'INST:SEL OUTP{self.index}')


    # channel voltage
    @property
    def voltage_V(self):
        result = self.ngu.query(f'MEAS:VOLT? (@{self.index})')
        return float(result)


    # channel current
    @property
    def current_A(self):
        result = self.ngu.query(f'MEAS:CURR? (@{self.index})')
        return float(result)
