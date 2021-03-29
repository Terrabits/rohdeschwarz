from .buffer       import Buffer
from .visa_library import VisaLibrary
from rohdeschwarz.bus.mixins.bus import BusMixin


class VisaBus(BusMixin):
    def __init__(self):
        self._visa         = VisaLibrary()
        self._buffer       = Buffer(size=1024)
        self.endline_byte  = b'\n'
        self._resource_mgr = None
        self._instr        = None

    def __del__(self):
        if self.is_open:
            self.close()

    # open/close
    def open(self, resource='tcpip::localhost::instr', timeout_ms=1000):
        if not self._resource_mgr:
            self._resource_mgr = self._visa.openDefaultRM()
        if not self._visa.is_success:
            self._resource_mgr = None
            return False
        self._instr = self._visa.open(self._resource_mgr, resource, timeout_ms)
        if not self._visa.is_success:
            self._instr = None
            return False
        self.timeout_ms = timeout_ms
        self._visa.set_termchar_en(self._instr, False)
        self._visa.set_send_end_en(self._instr, False)
        return True

    def close(self):
        self._visa.close(self._instr)
        self._instr = None

    @property
    def is_open(self):
        return self._instr is not None

    # timeout (ms)
    @property
    def timeout_ms(self):
        return self._timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, time_ms):
        self._visa.set_timeout_ms(self._instr, time_ms)
        self._timeout_ms = time_ms

    def _read_bytes_no_endline(self):
        return self._visa.read(self._instr, self._buffer)

    def _write_bytes_no_endline(self, data):
        return self._visa.write(self._instr, data)
