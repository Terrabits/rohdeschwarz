from rohdeschwarz.log import Log


class LogMixin:
    def __init__(self):
        self.log = Log()
        self.open_log      = self.log.open
        self.log_to_stdout = self.log.use_stdout
        self.close_log     = self.log.close

    def __del__(self):
        if self.log.is_open:
            self.log.close()

    @property
    def is_log(self):
        return self.log.is_open
