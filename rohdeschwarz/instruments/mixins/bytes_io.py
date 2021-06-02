class BytesIOMixin:
    def read_bytes(self, read_until_endline=True):
        data = self.bus.read_bytes(read_until_endline)
        self.log.print_read(data, self.bus.status_string())
        return data

    def write_bytes(self, data, add_endline=True):
        self.bus.write_bytes(data, add_endline)
        self.log.print_write(data, self.bus.status_string())
