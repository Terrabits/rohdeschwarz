import socket
from  .mixins.bus import BusMixin


class TcpBus(BusMixin):
    def __init__(self):
        self.buffer_size  = 1024
        self.endline_byte = b'\n'
        self._socket      = None

    def __del__(self):
        if self.is_open:
            self.close()

    # open/close
    def open(self, address='127.0.0.1', port=5025, timeout_ms=1000):
        self._socket    = socket.socket()
        self.timeout_ms = timeout_ms
        self._socket.connect((address, port))

    def close(self):
        self._socket.close()
        self._socket = None

    @property
    def is_open(self):
        return self._socket is not None

    # timeout (ms)
    @property
    def timeout_ms(self):
        if not self._socket.gettimeout():
            return 0
        return self._socket.gettimeout() * 1000

    @timeout_ms.setter
    def timeout_ms(self, value):
        self._socket.settimeout(value/1000)

    # connection status
    def status(self):
        # this is not applicable
        return None

    # helpers
    def _read_bytes_no_endline(self):
        return self._socket.recv(self.buffer_size)

    def _write_bytes_no_endline(self, data):
        self._socket.sendall(data)
