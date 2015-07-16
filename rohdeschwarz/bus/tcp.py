import socket

class TcpBus:
    def __init__(self):
        self.buffer_size = 1024
        self.delimiter = '\n' # Writes
        self._socket = None

    def __del__(self):
        if self._socket:
            self.close()

    def open(self, address='127.0.0.1', port=5025):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout_ms = 1000
        self._socket.connect((address, port))


    def close(self):
        self._socket.close()
        self._socket = None

    def read(self):
        result = self._socket.recv(self.buffer_size).decode()
        while not result.endswith(self.delimiter):
            result += self._socket.recv(self.buffer_size).decode()
        return result

    def write(self, buffer):
        if isinstance(buffer, str):
            buffer = buffer.encode()
        self.write_raw_no_end(buffer + self.delimiter.encode())

    def read_raw_no_end(self, buffer_size=1024):
        return self._socket.recv(buffer_size)

    def write_raw_no_end(self, buffer):
        if isinstance(buffer, str):
            buffer = buffer.encode()
        self._socket.send(buffer)

    def _timeout_ms(self):
        if not self._socket.gettimeout():
            return 0
        return self._socket.gettimeout() * 1000
    def _set_timeout_ms(self, value):
        self._socket.settimeout(value/1000)
    timeout_ms = property(_timeout_ms, _set_timeout_ms)

    def status_string(self):
        return None
