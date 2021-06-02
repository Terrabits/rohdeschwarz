class TimeoutMixin:
    @property
    def timeout_ms(self):
        return self.bus.timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, time_ms):
        self.bus.timeout_ms = time_ms
