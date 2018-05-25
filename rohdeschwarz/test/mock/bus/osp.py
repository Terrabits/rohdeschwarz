from rohdeschwarz.test.mock.bus.base import MockBus

import re

write_regex = r'^ROUT:CLOS \(@F(?P<instr>\d{2,2})A(?P<module>\d{2,2})\((?P<state>\d{2,2})(?P<switch>\d{2,2})\)\)$'
read_regex  = r'^ROUT:CLOS\? \(@F(?P<instr>\d{2,2})A(?P<module>\d{2,2})\((?P<state>\d{2,2})(?P<switch>\d{2,2})\)\)$'

class OspBus(MockBus):
    def __init__(self):
        super(OspBus, self).__init__()
        self.switches = {}
        self.reads  = []
        self.writes = []
        self.buffer = ''

    def read(self):
        if not self.buffer:
            raise Exception('Buffer empty')
        self.reads.append(self.buffer)
        self.buffer = ''
        return self.reads[-1]

    def write(self, scpi):
        write_match = re.match(write_regex, scpi)
        if write_match:
            self.writes.append(scpi)
            self.process_write(write_match)
            return
        read_match  = re.match(read_regex, scpi)
        if read_match:
            self.writes.append(scpi)
            self.buffer = self.process_read(read_match)
            return
        MockBus.write(self, scpi)

    def process_write(self, match):
        instr  = int(match.group('instr'))
        module = int(match.group('module'))
        switch = int(match.group('switch'))
        state  = int(match.group('state'))
        if not instr in self.switches:
            self.switches[instr] = {}
        instr = self.switches[instr]
        if not module in instr:
            instr[module] = {}
        module = instr[module]
        module[switch] = state

    def process_read(self, match):
        instr  = int(match.group('instr'))
        module = int(match.group('module'))
        switch = int(match.group('switch'))
        state  = int(match.group('state'))
        if not instr in self.switches:
            if state == 0:
                return '1'
            else:
                return '0'
        instr = self.switches[instr]
        if not module in instr:
            if state == 0:
                return '1'
            else:
                return '0'
        module = instr[module]
        if not switch in module:
            if state == 0:
                return '1'
            else:
                return '0'
        if module[switch] == state:
            return '1'
        else:
            return '0'
