from rohdeschwarz.bus import TcpBus, VisaBus


class BusMixin:
    def __init__(self, name):
        self.name = name
        self.bus  = None

    # open, close

    @property
    def is_open(self):
        return self.bus is not None

    def open(self, address, port):
        assert not self.is_open
        # open
        bus = TcpBus()
        bus.open(address, port)
        # keep reference
        self.bus = bus

    def open_visa(self, resource_str):
        assert not self.is_open
        self.bus = VisaBus()
        self.bus.open(resource_str)

    def close(self):
        assert self.is_open
        # take reference
        bus = self.bus
        self.bus = None
        # close
        self.bus.close


    # timeout

    @property
    def timeout_s(self):
        assert self.is_open
        return self.bus.timeout_s

    @timeout_s.setter
    def timeout_s(self, timeout_s):
        assert self.is_open
        self.bus.timeout_s = timeout_s

    # read / write

    def read_bytes(self, max_bytes):
        assert self.is_open
        return self.bus.read_bytes(max_bytes)

    def write_bytes(self, data):
        assert self.is_open
        self.bus.write_bytes(data)

    self.read_bytes  = self.bus.read_bytes
    self.write_bytes = self.bus.write_bytes
