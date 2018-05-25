class Marker(object):
    def __init__(self, vna, trace, index=1):
        super(Marker, self).__init__()
        self.vna   = vna
        self.trace = trace
        self.index = index

        self.name = 'M{0}'.format(index)
        self.x    = 0
        self.y    = 0

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
        self.trace.select_marker(self.index)
