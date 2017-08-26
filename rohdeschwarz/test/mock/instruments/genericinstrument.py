from rohdeschwarz.test.mock.bus  import FifoBus

class GenericInstrument:
    def __init__(self, id_string='', options_string=''):
        self.bus             = FifoBus()
        self._id_string      = id_string
        self._options_string = options_string
        self.errors          = []

    def open(self, *args):
        self.close()
        self.bus = FifoBus()
        self.bus.open(*args)
    def open_tcp(self, address):
        self.open(address)
    def close(self):
        if self.bus:
            self.bus.close()
        self.bus = None

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
