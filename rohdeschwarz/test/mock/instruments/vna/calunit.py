class CalUnit(object):
    def __init__(self, vna, name):
        super(CalUnit, self).__init__()
        self.vna   = vna
        self.name  = name
        self.ports = 4
        self.vna_ports_connected = []

    def __eq__(self, other):
        return str(self) == str(other)
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

    def select(self):
        self.vna.select_cal_unit(self.name)
