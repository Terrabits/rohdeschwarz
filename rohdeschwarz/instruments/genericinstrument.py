import numpy
import os
from rohdeschwarz.bus     import TcpBus, VisaBus
from rohdeschwarz.helpers import ellipsis_bytes, ellipsis_str
import sys


MAX_PRINT_LENGTH = 100


class GenericInstrument:
    def __init__(self):
        self.log = None
        self.bus = None

    def __del__(self):
        if self.is_open:
            self.close()

    # open/close
    def open(self, resource='tcpip::localhost::instr', timeout_ms=1000):
        self.bus = VisaBus()
        self.bus.open(resource, timeout_ms)

    def open_tcp(self, address='localhost', port=5025, timeout_ms=1000):
        self.bus = TcpBus()
        self.bus.open(address, port, timeout_ms)

    def close(self):
        self.bus.close()
        self.bus = None

    @property
    def is_open(self):
        return self.bus is not None

    # timeout (ms)
    @property
    def timeout_ms(self):
        return self.bus.timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, time_ms):
        self.bus.timeout_ms = time_ms

    # scpi log
    def open_log(self, filename):
        self.log = open(filename, 'w')
        if self.log.closed:
            sys.stderr.write(f"Could not open log '{filename}'\n")
            self.log = None

    def close_log(self):
        self.log.flush()
        self.log.close()
        self.log = None

    @property
    def is_log(self):
        return self.log is not None

    # instrument info
    def id_string(self):
        return self.query('*IDN?').strip()

    def options_string(self):
        return self.query("*OPT?").strip()

    def is_rohde_schwarz(self):
        return ("ROHDE" in self.id_string().upper())

    # errors
    def next_error(self):
        result  = self.query(':SYST:ERR?').strip()
        comma_index = result.find(',')
        code    = int(result[:comma_index])
        message = result[comma_index+2:-1]
        if code == 0:
            return None
        # else
        return code, message

    @property
    def errors(self):
        errors = [self.next_error()]
        while errors[-1] is not None:
            errors.append(self.next_error())
        errors.pop()
        return errors

    def is_error(self):
        return bool(self.errors)

    def clear_status(self):
        self.write("*CLS")

    # preset
    def preset(self):
        self.write("*RST")

    # local/remote
    def local(self):
        self.write("@LOC")

    def remote(self):
        self.write("@REM")

    # synchronization
    def wait(self):
        self.write('*WAI')

    def pause(self, timeout_ms=1000):
        '''*OPC?'''
        old_timeout     = self.timeout_ms
        self.timeout_ms = max(timeout_ms, self.timeout_ms)
        result = self.query('*OPC?').strip()
        self.timeout_ms = old_timeout
        return result == "1"

    def initialize_polling(self):
        '''*OPC'''
        self.write("*OPC")

    def is_operation_complete(self):
        '''*ESR? OPC bit == 1?'''
        opcBit = 1
        esr    = int(self.query('*ESR?').strip())
        return opcBit & esr > 0

    # str io
    def read(self):
        data = self.bus.read()
        self._print_read(data)
        return data

    def write(self, scpi_command):
        self.bus.write(scpi_command)
        self._print_write(scpi_command)

    def query(self, data):
        self.write(data)
        return self.read()

    # bytes io
    def read_bytes(self, read_until_endline=True)

    # TODO: clean these read/writes up
    def read_raw_no_end(self, buffer_size=102400):
        data = self.bus.read_raw_no_end(buffer_size)
        self._print_read(data)
        return data

    def write_raw_no_end(self, data):
        self.bus.write_raw_no_end(data)
        self._print_write(data)

    def query_raw_no_end(self, data, buffer_size=102400):
        self.write_raw_no_end(data)
        return self.read_raw_no_end(buffer_size)

    def read_block_data(self):
        data = self.read_raw_no_end()
        size, data = self.parse_block_data_header(data)
        while len(data) < size+1:
            data += self.read_raw_no_end()
        data = data[:size]
        return (size, data)

    def write_block_data(self, data):
        header = self.create_block_data_header(len(data))
        data = header + data
        self.write_raw_no_end(data)

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
            raise ValueError(0, "Expected array values of type 'float64'")
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
            raise ValueError(0, "Expected array values of type 'float64'")
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

    def _print_read(self, data):
        if not self.log or self.log.closed:
            return
        data = data.strip()
        if isinstance(data, str):
            if len(data) > self.MAX_PRINT:
                data = data[:self.MAX_PRINT]
                data += "..."
            self.log.write('Read:     "{0}"\n'.format(data))
        else:
            if len(data) > self.MAX_PRINT:
                data = data[:self.MAX_PRINT]
                data += b"..."
            self.log.write('Read:     {0}\n'.format(data))
        self.log.write('Bytes:    {0}\n'.format(len(data)))
        status = self.bus.status_string()
        if status:
            self.log.write('Status:   {0}\n'.format(status))
        self.log.write('\n')

    def _print_write(self, data):
        if not self.log or self.log.closed:
            return

        data = data.strip()
        if isinstance(data, str):
            data = ellipsis_str(data, MAX_PRINT_LENGTH)
        else:
        self.log.write(f'Write:    "{data}"\n')
        self.log.write('Bytes:    {0}\n'.format(len(data)))
        status = self.bus.status_string()
        if status:
            self.log.write('Status:   {0}\n'.format(status))
        self.log.write('\n')
