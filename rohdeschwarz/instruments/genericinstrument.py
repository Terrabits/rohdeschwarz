import sys
import os
#import struct
import numpy
from rohdeschwarz.general import ConnectionMethod
from rohdeschwarz.bus.tcp import TcpBus
from rohdeschwarz.bus.visa import VisaBus


class GenericInstrument(object):
    _MAX_PRINT = 100

    def __init__(self):
        self.log = None
        self.bus = None
        self.buffer_size = 1024
        self.connection_method = ''
        self.address = ''
        self.bytes_transferred = 0

    def __del__(self):
        self.close()

    def open(self, connection_method = ConnectionMethod.tcpip, address = '127.0.0.1'):
        self.bus = VisaBus()
        self.bus.open(connection_method, address)

    def open_tcp(self, ip_address='127.0.0.1', socket=5025):
        self.connection_method = ConnectionMethod.tcpip
        self.address = "{0}:{1}".format(ip_address, socket)
        self.bus = TcpBus()
        self.bus.open(ip_address, socket)

    def close(self):
        if self.bus:
            self.bus.close()
            self.bus = None

    def connected(self):
        if not self.bus:
            return False
        try:
            return len(self.id_string()) > 0
        except:
            return False
        # Else
        return True

    def _timeout_ms(self):
        return self.bus.timeout_ms
    def _set_timeout_ms(self, time):
        self.bus.timeout_ms = time
    timeout_ms = property(_timeout_ms, _set_timeout_ms)

    def open_log(self, filename):
        self.log = open(filename, 'w')
        if self.log.closed:
            message = "Could not open log at '{0}'\n"
            message = message.format(filename)
            sys.stderr.write(message)
            self.log = None

    def close_log(self):
        if self.log:
            self.log.flush()
            self.log.close()
            self.log = None

    def id_string(self):
        return self.query('*IDN?').strip()

    def options_string(self):
        return self.query("*OPT?").strip()

    def clear_status(self):
        self.write("*CLS")

    def preset(self):
        self.write("*RST")

    def local(self):
        self.write("@LOC")

    def remote(self):
        self.write("@REM")

    def is_rohde_schwarz(self):
        return ("ROHDE" in self.id_string().upper())

    def wait(self):
        self.write('*WAI')

    def pause(self, timeout_ms=1000):
        old_timeout = self.timeout_ms
        self.timeout_ms = timeout_ms
        result = self.query('*OPC?').strip() == "1"
        self.timeout_ms = old_timeout
        return result

    def initialize_polling(self):
        self.write("*OPC")

    def is_operation_complete(self):
        opcBit = 1
        esr = int(self.query('*ESR?').strip())
        return opcBit & esr > 0

    def print_info(self):
        _log = self.log
        self.log = None
        _log.write('INSTRUMENT INFO\n')
        _log.write('Connection: {0}\n'.format(self.connection_method))
        _log.write('Address:    {0}\n'.format(self.address))
        if self.is_rohde_schwarz():
            _log.write('Make:       Rohde & Schwarz\n')
        else:
            _log.write('Make:       Unknown\n')
        _log.write('Id string:  {0}\n\n'.format(self.id_string()))
        self.log = _log

    def read(self):
        buffer = self.bus.read()
        self.bytes_transferred = len(buffer)
        self._print_read(buffer)
        return buffer

    def write(self, buffer):
        self.bus.write(buffer)
        self.bytes_transferred = len(buffer)
        self._print_write(buffer)

    def query(self, buffer):
        self.write(buffer)
        return self.read()

    def read_raw_no_end(self, buffer_size=102400):
        buffer = self.bus.read_raw_no_end(buffer_size)
        self.bytes_transferred = len(buffer)
        self._print_read(buffer)
        return buffer

    def write_raw_no_end(self, buffer):
        self.bus.write_raw_no_end(buffer)
        self.bytes_transferred = len(buffer)
        self._print_write(buffer)

    def query_raw_no_end(self, buffer, buffer_size=102400):
        self.write_raw_no_end(buffer)
        return self.read_raw_no_end(buffer_size)

    def read_block_data(self):
        buffer = self.read_raw_no_end()
        size, buffer = self.parse_block_data_header(buffer)
        while len(buffer) < size+1:
            buffer += self.read_raw_no_end()
        buffer = buffer[:size]
        return (size, buffer)

    def write_block_data(self, buffer):
        header = self.create_block_data_header(len(buffer))
        buffer = header + buffer
        self.write_raw_no_end(buffer)

    def read_block_data_to_file(self, filename, buffer_size=102400):
        if buffer_size < 11:
            buffer_size = 11
        data = self.read_raw_no_end(buffer_size)
        size, data = self.parse_block_data_header(data)
        if len(data) > size:
            data = data[:size]
        with open(filename, 'wb') as file:
            file.write(data)
            size -= len(data)
            while size > 0:
                data = self.read_raw_no_end(buffer_size)
                if len(data) > size:
                    data = data[:size]
                file.write(data)
                size -= len(data)

    def write_block_data_from_file(self, filename, buffer_size=1024*1024):
        header = self.create_block_data_header(os.path.getsize(filename))
        self.write_raw_no_end(header)
        with open(filename, 'rb') as file:
            data = file.read(buffer_size)
            while data:
                print('Writing: {0}'.format(len(data)))
                self.write_raw_no_end(data)
                data = file.read(buffer_size)
        self.write_raw_no_end('\n') # Firmware won't move until to confirm end somehow

    def read_64_bit_vector_block_data(self):
        size, buffer = self.read_block_data()
        return numpy.frombuffer(buffer, 'float64')

    def write_64_bit_vector_block_data(self, data):
        if not isinstance(data, numpy.ndarray):
            raise ValueError(0, 'Expected numpy.ndarray')
        if data.dtype != 'float64':
            raise valueError(0, "Expected array values of type 'float64'")
        data = data.tobytes()
        header = self.create_block_data_header(len(data))
        data = header + data
        self.write_raw_no_end(data)

    def read_64_bit_complex_vector_block_data(self):
        buffer = self.read_64_bit_vector_block_data()
        return numpy.frombuffer(buffer, 'complex128')

    def write_64_bit_complex_vector_block_data(self, data):
        if not isinstance(data, numpy.ndarray):
            raise ValueError(0, 'Expected numpy.ndarray')
        if data.dtype != 'complex128':
            raise valueError(0, "Expected array values of type 'float64'")
        data = data.tobytes()
        header = self.create_block_data_header(len(data))
        data = header + data
        self.write_raw_no_end(data)

    def parse_block_data_header(self, buffer):
        if buffer[0:1] != b'#':
            raise ValueError(0, 'Not bytes in IEEE 488.2 block data format')
        header_size = 2 + int(buffer[1:2])
        header = buffer[:header_size]
        buffer = buffer[header_size:]
        size = int(header[2:])
        return (size, buffer)

    def create_block_data_header(self, buffer_length):
        size_string = str(buffer_length)
        result = "#" + str(len(size_string)) + size_string
        return result.encode()

    def _print_read(self, buffer):
        if not self.log or self.log.closed:
            return
        buffer = buffer.strip()
        if isinstance(buffer, str):
            if len(buffer) > self._MAX_PRINT:
                buffer = buffer[:self._MAX_PRINT]
                buffer += "..."
            self.log.write('Read:     "{0}"\n'.format(buffer))
        else:
            if len(buffer) > self._MAX_PRINT:
                buffer = buffer[:self._MAX_PRINT]
                buffer += b"..."
            self.log.write('Read:     {0}\n'.format(buffer))
        self.log.write('Bytes:    {0}\n'.format(self.bytes_transferred))
        status = self.bus.status_string()
        if status:
            self.log.write('Status:   {0}\n'.format(status))
        self.log.write('\n')

    def _print_write(self, buffer):
        if not self.log or self.log.closed:
            return
        buffer = buffer.strip()
        if isinstance(buffer, str):
            if len(buffer) > self._MAX_PRINT:
                buffer = buffer[:self._MAX_PRINT]
                buffer += "..."
            self.log.write('Write:    "{0}"\n'.format(buffer))
        else:
            if len(buffer) > self._MAX_PRINT:
                buffer = buffer[:self._MAX_PRINT]
                buffer += b"..."
            self.log.write('Write:    {0}\n'.format(buffer))
        self.log.write('Bytes:    {0}\n'.format(self.bytes_transferred))
        status = self.bus.status_string()
        if status:
            self.log.write('Status:   {0}\n'.format(status))
        self.log.write('\n')
