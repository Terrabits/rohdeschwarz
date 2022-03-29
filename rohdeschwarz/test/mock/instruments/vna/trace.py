from numpy        import array
from numpy.random import default_rng
from rohdeschwarz.test.mock.instruments.vna.marker import Marker


# variables
generator = default_rng()


# helpers

def random_numbers(count):
    return generator.standard_normal(count)


def random_complex_numbers(count):
    real = random_numbers(count)
    imag = random_numbers(count) * 1j
    return  real + imag


class Trace(object):
    def __init__(self, vna, name, channel, parameter):
        super(Trace, self).__init__()
        self.vna       = vna
        self.name      = name
        self.channel   = channel
        self.diagram   = None
        self.parameter = parameter
        self.format    = 'MLOG'

        self.selected_marker = None
        self.mock_markers    = []

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

    @property
    def y_formatted(self):
        channel = self.vna.channel(self.channel)
        points  = channel.points
        return random_numbers(points)

    @property
    def y_complex(self):
        channel = self.vna.channel(self.channel)
        points  = channel.points
        return random_complex_numbers(points)

    def is_marker(self, index):
        return index in self.mock_markers

    def create_marker(self, index):
        if not index in self.mock_markers:
            self.mock_markers.append(Marker(self.vna, self.name, index))
            self.mock_markers.sort()

    def delete_marker(self, index):
        if index in self.mock_markers:
            self.mock_markers.remove(index)

    def delete_markers(self):
        self.mock_markers.clear()

    def _markers(self):
        return [int(i) for i in self.mock_markers]
    def _set_markers(self, markers):
        for i in markers:
            if not self.is_marker(i):
                self.create_marker(i)
    markers = property(_markers, _set_markers)

    def marker(self, index=1):
        return self.mock_markers[self.mock_markers.index(index)]
