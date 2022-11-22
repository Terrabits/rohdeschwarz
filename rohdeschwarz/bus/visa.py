from   .helpers             import ignore_warnings
import pyvisa
from   pyvisa.errors        import VisaIOError
import pyvisa.ctwrapper.functions as vi


class VisaBus:
    def __init__(self):
        self.instr    = None
        self.session  = None
        self.visa_lib = None

    # open / close

    @property
    def is_open(self):
        return self.instr is not None

    def open(self, resource_str):
        assert not self.is_open
        # open
        resource_mgr = pyvisa.ResourceManager()
        instr = resource_mgr.open_resource(resource_str)

        # do not add line endings
        self.disable_term_chars()

        # keep references
        self.instr    = instr
        self.session  = self.instr.session
        self.visa_lib = resource_mgr.visalib

    def close(self):
        assert self.is_open
        # take references
        instr         = self.instr
        self.instr    = None
        self.session  = None
        self.visa_lib = None
        # close
        instr.close()

    # timeout (seconds)

    @property
    def timeout_s(self):
        return self.instr.timeout

    @timeout_s.setter
    def timeout_s(self, timeout_s):
        self.instr.timeout = timeout_s

    # bytes IO

    @ignore_warnings
    def read_bytes(self, max_bytes):
        result = vi.read(self.visa_lib, self.session, max_bytes)
        return result[0]

    def write_bytes(self, data):
        vi.write(self.visa_lib, self.session, data)

    # helpers

    def log_status(self):
        """logs VISA status code and description"""
        result = '{0} {1} {2}'
        value = self.instr.last_status.value
        status = VisaIOError(value)
        return result.format(hex(value), status.abbreviation, status.description)
