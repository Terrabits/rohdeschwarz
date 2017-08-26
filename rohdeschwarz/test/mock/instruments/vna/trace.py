class Trace:
    def __init__(self, vna, name, channel, parameter):
        self.vna       = vna
        self.name      = name
        self.channel   = channel
        self.diagram   = None
        self.parameter = parameter

    def __lt__(self, other):
        return str(self).lower() < str(other).lower()
    def __eq__(self, other):
        return str(self) == str(other)
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

    def select(self):
        self.vna.select_trace(self)
