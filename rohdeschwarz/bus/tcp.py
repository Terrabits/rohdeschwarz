from socket import socket


class TcpBus:
    """instrument bus class for TCP sockets"""
    def __init__(self):
        self.socket = None

    # open / close

    @property
    def is_open(self):
        return self.socket is not None

    def open(self, address, port):
        assert not self.is_open
        # open
        s = socket()
        s.timeout_ms = 1000
        s.connect((address, port))

        # keep reference
        self.socket = s

    def close(self):
        assert self.is_open
        # take reference
        s = self.socket
        self.socket = None
        # close
        s.close()

    @property
    def timeout_s(self):
        assert self.is_open
        timeout = self.socket.gettimeout()
        return 0 if timeout is None else float(timeout)

    @timeout_s.setter
    def timeout_s(self, timeout_s):
        assert self.is_open
        # 0 s timeout means infinite timeout
        # therefore: timeout should be `None`
        timeout_s = None if timeout_s == 0 else timeout_ms
        self.socket.settimeout(timeout_s)

    # bytes IO

    def read_bytes(self, max_bytes):
        assert self.is_open
        return self.socket.recv(max_bytes)

    def write_bytes(self, data):
        assert self.is_open
        self.socket.sendall(data)
