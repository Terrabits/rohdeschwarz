class SynchronizationMixin:
    # tell parser to handle synchronization
    def wait(self):
        '''send *WAI? to indicate parser should process all commands before continuing.'''
        self.write('*WAI')


    # synchronize with instrument (or timeout)
    def pause(self, timeout_ms=1000):
        '''query *OPC? and block until complete'''
        old_timeout     = self.timeout_ms
        self.timeout_ms = max(timeout_ms, self.timeout_ms)
        result = self.query('*OPC?').strip()
        self.timeout_ms = old_timeout
        return result == "1"


    # poll-and-loop
    # start
    def initialize_polling(self):
        '''*OPC'''
        self.write("*OPC")

    # done?
    @property
    def is_operation_complete(self):
        '''*ESR? OPC bit == 1?'''
        opcBit = 1
        esr    = int(self.query('*ESR?').strip())
        return opcBit & esr > 0
