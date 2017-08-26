class Channel:
    def __init__(self, vna, index):
        self.vna  = vna
        self.index = index
        self.name  = 'Ch{0}'.format(index)

    def __int__(self):
        return self.index
    def __lt__(self, other):
        return int(self) < int(other)
    def __eq__(self, other):
        return int(self) == int(other)
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

    def select(self):
        self.vna.select_channel(int(self))

    def _traces(self):
        traces = []
        for i in self.vna.traces:
            if self.vna.trace(i).channel == self.index:
                traces.append(i)
        return traces
    traces = property(_traces)

    def sweep(self):
        pass

    def auto_calibrate(self, ports, characterization=''):
        cu = self.vna.selected_cal_unit
        cu = self.vna.cal_unit(cu)
        for p in ports:
            if not p in cu.vna_ports_connected:
                msg = 'Port {0} not connected to cal unit'
                msg = msg.format(p)
                raise Exception(msg)
