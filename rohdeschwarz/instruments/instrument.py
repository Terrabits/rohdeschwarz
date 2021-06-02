from .mixins          import InstrumentMixin
from io               import StringIO
from rohdeschwarz.bus import TcpBus, VisaBus


class Instrument(InstrumentMixin):
    # constructor/destructor
    def __init__(self):
        InstrumentMixin.__init__(self)
        self.bus = None

    def __del__(self):
        if self.is_open:
            self.close()
        InstrumentMixin.__del__(self)

    # instrument connection
    @property
    def is_open(self):
        return self.bus is not None

    def open(self, resource='tcpip::localhost::instr', timeout_ms=1000):
        self.bus = VisaBus()
        self.bus.open(resource, timeout_ms)

    def open_tcp(self, address='localhost', port=5025, timeout_ms=1000):
        self.bus = TcpBus()
        self.bus.open(address, port, timeout_ms)

    def close(self):
        self.bus.close()
        self.bus = None

    # log
    def print_info(self):
        self.log.pause()

        info = StringIO()
        if self.is_open:
            info.write( 'Instrument Info\n')
            info.write(f'*IDN?\n  {self.id_string.strip()}\n')
            info.write(f'*OPT?\n  {self.options_string.strip()}\n')
        else:
            info.write( 'Instrument not found!\n')
            info.write(f'Connection:       {self.connection_method}\n')
            info.write(f'Address:          {self.address}\n')
        info.write('\n')

        self.log.resume()
        self.log.print(info.getvalue())

    # is rohde instrument?
    @property
    def is_rohde_schwarz(self):
        return ("rohde" in self.id_string.lower())
