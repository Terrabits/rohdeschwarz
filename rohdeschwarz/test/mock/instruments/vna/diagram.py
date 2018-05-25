class Diagram(object):
    def __init__(self, vna, index):
        super(Diagram, self).__init__()
        self.vna   = vna
        self.index = index
        self.title = ''

    def __int__(self):
        return self.index
    def __lt__(self, other):
        return int(self) < int(other)
    def __eq__(self, other):
        return int(self) == int(other)
    def __repr__(self):
        return str(int(self))

    def _traces(self):
        traces = []
        for i in self.vna.traces:
            if self.vna.trace(i).diagram == self.index:
                traces.append(i)
        return traces
