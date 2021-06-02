class StringIOMixin:
    def read(self):
        data = self.bus.read()
        self.log.print_read(data, self.bus.status_string())
        return data

    def write(self, scpi_command):
        self.bus.write(scpi_command)
        self.log.print_write(scpi_command, self.bus.status_string())

    def query(self, data):
        self.write(data)
        return self.read()
