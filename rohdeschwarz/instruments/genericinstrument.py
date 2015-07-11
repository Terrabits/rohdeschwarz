import sys
import visa
from pyvisa.errors import VisaIOError
import pyvisa.resources as visa_resources
import socket
import re
from rohdeschwarz.general import ConnectionMethod
from rohdeschwarz.bus.tcp import TcpBus


class GenericInstrument:
    _MAX_PRINT = 100

    def __init__(self):
        self.log = None
        self.bus = None
        self.connection_method = ''
        self.address = ''
        self.bytes_transferred = 0

    def __del__(self):
        if self.bus:
            self.bus.close()
            self.bus = None

    def open(self, connection_method = ConnectionMethod.tcpip, address = '127.0.0.1'):
        self.connection_method = connection_method
        self.address = address
        resource_string = "{0}::{1}::INSTR".format(connection_method, address)
        self.bus = visa.ResourceManager().open_resource(resource_string)

    def open_tcp(self, ip_address='127.0.0.1', socket=5025):
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

    def open_log(self, filename):
        self.log = open(filename, 'w')
        if self.log.closed:
            message = "Could not open log at '{0}'\n"
            message = message.format(filename)
            sys.stderr.write(message)
            self.log = None

    def close_log(self):
        if self.log:
            self.log.close()
            self.log = None

    def id_string(self):
        return self.query('*IDN?')

    def options_string(self):
        return self.query("*OPT?")

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
        old_timeout = self.bus.timeout
        self.bus.timeout = timeout_ms
        result = self.query('*OPC?').strip() == "1"
        self.bus.timeout = old_timeout
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

    def last_status_bytes(self):
        return self.bytes_transferred

    def last_status_value(self):
        return self.bus.last_status.value

    def last_status_name(self):
        return self.bus.last_status.name

    def read(self):
        buffer = self.bus.read()
        self.bytes_transferred = len(buffer)
        self._print_read(buffer)
        return buffer

    def write(self, buffer):
        self.last_status = self.bus.write(buffer)
        self.bytes_transferred = len(buffer)
        self._print_write(buffer)

    def query(self, buffer):
        self.write(buffer)
        return self.read()

    def _print_read(self, buffer):
        if not self.log or self.log.closed:
            return
        buffer = buffer.strip()
        if len(buffer) > self._MAX_PRINT:
            buffer = buffer[:self._MAX_PRINT] + '...'
        self.log.write('Read:     "{0}"\n'.format(buffer))
        if self._is_visa():
            self.log.write(self.status())
            self.log.write('\n')

    def _print_write(self, buffer):
        if not self.log or self.log.closed:
            return
        buffer = buffer.strip()
        if len(buffer) > self._MAX_PRINT:
            buffer = buffer[:self._MAX_PRINT] + '...'
        self.log.write('Write:    "{0}"\n'.format(buffer))
        if self._is_visa():
            self.log.write(self.status())
            self.log.write('\n')

    def _is_visa(self):
        types = (visa_resources.SerialInstrument, \
                 visa_resources.TCPIPInstrument, \
                 visa_resources.TCPIPSocket, \
                 visa_resources.USBInstrument, \
                 visa_resources.USBRaw, \
                 visa_resources.GPIBInstrument, \
                 visa_resources.GPIBInterface, \
                 visa_resources.FirewireInstrument, \
                 visa_resources.PXIInstrument, \
                 visa_resources.PXIInstrument, \
                 visa_resources.VXIInstrument, \
                 visa_resources.VXIMemory, \
                 visa_resources.VXIBackplane)
        return isinstance(self.bus ,types)

    def status(self):
        result = 'Bytes:    {0}\n'.format(self.bytes_transferred)
        visa_io_error = VisaIOError(self.last_status_value())
        result +='Status:   {0} {1} {2}\n'.format(hex(self.last_status_value()), visa_io_error.abbreviation, visa_io_error.description)
        return result
