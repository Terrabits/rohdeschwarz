class Channel(object):
    def __init__(self, vna, index):
        super(Channel, self).__init__()
        self.vna                = vna
        self.index              = index
        self.name               = 'Ch{0}'.format(index)
        self.start_frequency_Hz = 100e3
        self.stop_frequency_Hz  = 8e9
        self.points             = 101
        self.if_bandwidth_Hz    = 10e3
        self.power_dBm          = 0.0
        self.cal_group          = None

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

    def save_cal(self, name):
        if not name.lower() in self.vna.cal_groups:
            self.vna.cal_groups.append(name)
            self.vna.cal_groups.sort()

    def auto_calibrate(self, ports, characterization=''):
        cal_unit = self.vna.selected_cal_unit
        cal_unit = self.vna.cal_unit(cal_unit)
        for port in ports:
            if not port in cal_unit.vna_ports_connected:
                msg = 'Port {0} not connected to cal unit'
                msg = msg.format(p)
                raise Exception(msg)
