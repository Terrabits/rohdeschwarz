

class StringIOMixin:
    # requires read_bytes, write_bytes (BytesIOMixin)
    def read(self):
        data = self.read_bytes()
        return data.decode()

    def write(self, scpi_command):
        data = scpi_command.encode()
        self.write_bytes(data)

    def query(self, scpi):
        self.write(scpi)
        return self.read()
