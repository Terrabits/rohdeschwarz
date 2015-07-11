import socket

class TcpBus:
    def __init__(self):
        self.buffer_size = 1024
        self._socket = None

    def __del__(self):
        if self._socket:
            self._socket.close()
            self._socket = None

    def open(self, address='127.0.0.1', port=5025):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))
        self.timeout = 1000

    def close(self):
        self._socket.close()
        self._socket = None

    def write(self, buffer):
        self._socket.send(buffer.encode() + b'\n')

    def read(self):
        return self._socket.recv(self.buffer_size).decode()

    def _timeout(self):
        if not self._socket.gettimeout():
            return 0
        return self._socket.gettimeout() * 1000
    def _set_timeout(self, value):
        self._socket.settimeout(value/1000)
    timeout = property(_timeout, _set_timeout)
