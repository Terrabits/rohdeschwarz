from   .mixins              import QueryMixin
from   rohdeschwarz.general import ConnectionMethod
import pyvisa
from   pyvisa.errors        import VisaIOError
import pyvisa.ctwrapper.functions as vi
import warnings


class VisaBus(QueryMixin):
    """
    VisaBus is a wrapper for pyvisa for compatibility with
    the rohdeschwarz.instruments.genericinstrument genericinstrument
    base class

    Example:
        from rohdeschwarz.general import ConnectionMethod
        connection_method = ConnectionMethod.gpib
        address = '17'

        bus = VisaBus()
        bus.open(connection_method, address)

        # Optional parameters
        bus.timeout_ms = 2000

        # Read/write strings
        # (delimiter is sent)
        bus.write('*IDN?')
        print('ID: ' + bus.read())

        # Read/write binary data
        # Delimiter ('send_end') not used
        bus.write_raw_no_end(b'#3256...')

        # Retrieve bus status
        print(bus.status())
        #
    """
    def __init__(self):
        """
        Constructor
        """
        super(VisaBus, self).__init__()
        self._instr = None
        self._session = None
        self._visa_lib = None

    def __del__(self):
        if self._instr:
            self.close()

    def open(self, connection_method = ConnectionMethod.tcpip, address = '127.0.0.1'):
        """
        Open instrument connection.
        Args:
            connection_method (ConnectionMethod(Enum) or str)
            address (str)
        Raises:
            VisaIOError: if instrument not found
        """
        resource_string = "{0}::{1}::INSTR".format(connection_method, address)
        rm = pyvisa.ResourceManager()
        instr = rm.open_resource(resource_string)
        self._instr = instr
        self._session = self._instr.session
        self._visa_lib = rm.visalib

    def close(self):
        """
        Close instrument connection
        """
        if self._instr:
            self._instr.close()
            self._instr = None

    def read(self):
        """
        Read until send_end '\n' is reached

        Returns:
            str

        Raises:
            VisaIOError: if instrument not found
        """
        return self._instr.read()

    def write(self, buffer):
        """
        Write 'buffer' to instrument, followed by send_end '\n'

        Args:
            buffer (str): to be written

        Raises:
            VisaIOError: if instrument not found
        """
        self._instr.write(buffer)

    def read_raw_no_end(self, buffer_size=1024):
        """
        Read up to 'buffer_size' binary bytes

        Args:
            buffer_size (int): bytes

        Returns:
            bytes (b'...')

        Raises:
            VisaIOError: if instrument not found
        """
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
        """
        Writes binary data in 'buffer' to instrument

        Args:
            buffer (bytes, b'...'): to be written

        Raises:
            VisaIOError: if instrument not found
        """
        if not isinstance(buffer, bytes):
            buffer = bytes(buffer, 'utf-8')
        send_end = self._instr.send_end
        write_term = self._instr.write_termination
        self._instr.send_end = None
        self._instr.write_termination = None
        vi.write(self._visa_lib, self._session, buffer)
        self._instr.send_end = send_end
        self._instr.write_termination = write_term

    def _timeout_ms(self):
        """
        timeout

        Args:
            timeout (int): milliseconds

        Returns:
            timeout (int): milliseconds

        """
        return self._instr.timeout
    def _set_timeout_ms(self, time_ms):
        self._instr.timeout = time_ms
    timeout_ms = property(_timeout_ms, _set_timeout_ms)

    def status_string(self):
        """
        Status code and human-readable status string
        for the VISA bus

        Returns:
            str: Status string

        Example:
            '0x0 VI_SUCCESS Operation completed successfully.'
        """
        result = '{0} {1} {2}'
        value = self._instr.last_status.value
        status = VisaIOError(value)
        return result.format(hex(value), status.abbreviation, status.description)
