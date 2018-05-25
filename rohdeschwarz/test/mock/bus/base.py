import re

id_regex  = r'\*IDN\?'
opc_regex = r'\*OPC\?'

class MockBus(object):
    def __init__(self):
        super(MockBus, self).__init__()
        self.reads  = []
        self.writes = []
        self.buffer = ''
        self.timeout_ms = 1000

    def open(self, *argv):
        pass

    def close(self):
        pass

    def status_string(self):
        return "MockBus is always doing fine"

    def read(self):
        if not self.buffer:
            raise Exception('Buffer empty')
        self.reads.append(self.buffer)
        self.buffer = ''
        return self.reads[-1]

    def write(self, scpi):
        self.writes.append(scpi)
        if re.match(id_regex, scpi):
            self.buffer = 'rohdeschwarz.test.mock.bus'
        elif re.match(opc_regex, scpi):
            self.buffer = '1'

    def read_raw_no_end(self):
        return self.read()

    def write_raw_no_end(self, scpi):
        self.write(scpi)
