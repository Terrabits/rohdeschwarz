from rohdeschwarz.test.mock.bus  import FifoBus

class GenericInstrument(object):
    def __init__(self, id_string='Rohde-Schwarz,Instrument,1,1.0.0', options_string=''):
        super(GenericInstrument, self).__init__()
        self.bus     = None
        self.log     = None
        self.id      = id_string
        self.options = options_string
        self.errors  = []
        self.timeout_ms = 1000
        self._operation_complete = False


    def open(self, *args):
        if self.bus:
            self.close()
        self.bus = FifoBus()
        self.bus.open(*args)

    def open_tcp(self, ip_address='127.0.0.1', socket=5025):
        self.open(ip_address, socket)

    def close(self):
        if self.bus:
            self.bus.close()
        self.bus = None

    def connected(self):
        return self.bus is not None

    def open_log(self, filename):
        self.log = filename

    def close_log(self):
        pass

    def read(self):
        return self.bus.read()
    def write(self, scpi):
        self.bus.write(scpi)
    def query(self, scpi):
        self.write(scpi)
        return self.read()

    def id_string(self):
        return self.id

    def options_string(self):
        return self.options

    def preset(self):
        pass

    def is_error(self):
        return bool(self.errors)

    def clear_status(self):
        self.errors = []

    def remote(self):
        pass

    def local(self):
        pass


    # operation status

    def initialize_polling(self):
        self._operation_complete = False

    def is_operation_complete(self):
        return self._operation_complete

    def wait(self):
        self._operation_complete = True

    def pause(self, timeout_ms=1000):
        self._operation_complete = True
        return True


    def print_info(self):
        pass
