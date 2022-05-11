from ..socket import Socket


class SocketMixin:
    def __init__(self, name):
        self.socket = Socket(name)
        self.open   = self.socket.open
        self.close  = self.socket.close
        self.read_bytes  = self.socket.read_bytes
        self.write_bytes = self.socket.write_bytes

    # open, close

    @property
    def is_open(self):
        return self.socket.is_open

    # timeout

    @property
    def timeout_s(self):
        assert self.is_open
        return self.socket.timeout_s

    @timeout_s.setter
    def timeout_s(self, timeout_s):
        assert self.is_open
        self.socket.timeout_s = timeout_s
