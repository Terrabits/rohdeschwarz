import socket

class TcpBus:
    """
    TcpBus provides a VISA-like interface for an instrument
    connection using TCP sockets.

    Example:
        address = '192.168.35.5'
        port    =  5025

        TcpBus bus()
        bus.open(address, port)

        # Optional parameters
        # These are the default values:
        bus.buffer_size = 1024
        bus.delimiter = '\n'

        # Read/write strings
        # (delimiter is sent)
        bus.write('*IDN?')
        print('ID: ' + bus.read())

        # Read/write binary data
        # (delimiter not used)
        bus.write(b'#3256...')

    """

    def __init__(self):
        """ Initialize new TcpBus (no arguments) """
        self.buffer_size = 1024
        self.delimiter = '\n' # Writes
        self._socket = None

    def __del__(self):
        if self._socket:
            self.close()

    def open(self, address='127.0.0.1', port=5025):
        """
        Open TCP socket connection.
        Raises socket.timeout if instrument not found
        Args:
            address (str)
            port (int)

        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout_ms = 1000
        self._socket.connect((address, port))


    def close(self):
        """ Close connection """
        self._socket.close()
        self._socket = None

    def read(self):
        """ Read until delimter is received """
        result = self._socket.recv(self.buffer_size).decode()
        while not result.endswith(self.delimiter):
            result += self._socket.recv(self.buffer_size).decode()
        return result

    def write(self, buffer):
        """
        Write 'buffer' + delimiter
        Args:
            buffer (bytes: b'...')
        """
        if isinstance(buffer, str):
            buffer = buffer.encode()
        self.write_raw_no_end(buffer + self.delimiter.encode())

    def read_raw_no_end(self, buffer_size=1024):
        """
        Read up to 'buffer_size' bytes
        Args:
            buffer_size (int): buffer size in bytes
        """
        return self._socket.recv(buffer_size)

    def write_raw_no_end(self, buffer):
        """
        Write 'buffer' without delimiter
        Args:
            buffer (bytes, b'...')
        """
        if isinstance(buffer, str):
            buffer = buffer.encode()
        self._socket.send(buffer)

    def _timeout_ms(self):
        """ Timeout value, in milliseconds """
        if not self._socket.gettimeout():
            return 0
        return self._socket.gettimeout() * 1000
    def _set_timeout_ms(self, value):
        self._socket.settimeout(value/1000)
    timeout_ms = property(_timeout_ms, _set_timeout_ms)


    def status_string(self):
        """ Included for compatibility purposes (returns None) """
        return None
