
class MockBus:
    def __init__(self):
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
        else:
            self.reads.append(self.buffer)
            self.buffer = ''
            return self.reads[-1]

    def read_raw_no_end(self):
        return self.read()

    def write_raw_no_end(self, scpi):
        self.write(scpi)
