from rohdeschwarz.test.mock.bus  import FifoBus

class GenericInstrument(object):
    def __init__(self, id_string='', options_string=''):
        super(GenericInstrument, self).__init__()
        self.bus             = FifoBus()
        self._id_string      = id_string
        self._options_string = options_string
        self.errors          = []
        self.timeout_ms      = 1000

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
        return bool(self.bus)

    def open_log(self, filename):
        pass
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
        return self._id_string
    def options_string(self):
        return self._options_string
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

    def wait(self):
        pass
    def pause(self, timeout_ms=1000):
        return True

    def print_info(self):
        pass
