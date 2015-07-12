from rohdeschwarz.general import ConnectionMethod
import visa
from pyvisa.errors import VisaIOError
import pyvisa.ctwrapper.functions as vi
import warnings

class VisaBus:
    def __init__(self):
        self._instr = None
        self._session = None
        self._visa_lib = None

    def __del__(self):
        if self._instr:
            self.close()

    def open(self, connection_method = ConnectionMethod.tcpip, address = '127.0.0.1'):
        resource_string = "{0}::{1}::INSTR".format(connection_method, address)
        rm = visa.ResourceManager()
        self._instr = rm.open_resource(resource_string)
        self._session = self._instr.session
        self._visa_lib = rm.visalib

    def close(self):
        self._instr.close()
        self._instr = None

    def read(self):
        return self._instr.read()

    def write(self, buffer):
        self._instr.write(buffer)

    def read_raw_no_end(self, buffer_size=1024):
        send_end = self._instr.send_end
        read_term = self._instr.read_termination
        self._instr.send_end = None
        self._instr.read_termination = None
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = vi.read(self._visa_lib, self._session, buffer_size)
        self._instr.send_end = send_end
        self._instr.read_termination = read_term
        return result[0]

    def write_raw_no_end(self, buffer):
        send_end = self._instr.send_end
        write_term = self._instr.write_termination
        self._instr.send_end = None
        self._instr.write_termination = None
        vi.write(self._visa_lib, self._session, buffer)
        self._instr.send_end = send_end
        self._instr.write_termination = write_term

    def _timeout_ms(self):
        return self._instr.timeout
    def _set_timeout_ms(self, time_ms):
        self._instr.timeout = time_ms
    timeout_ms = property(_timeout_ms, _set_timeout_ms)

    def status_string(self):
        result = '{0} {1} {2}'
        value = self._instr.last_status.value
        status = VisaIOError(value)
        return result.format(hex(value), status.abbreviation, status.description)


