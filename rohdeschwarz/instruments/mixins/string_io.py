class StringIOMixin:
    def read(self):
        # read bytes
        data = self.read_bytes()
        return data.strip().decode()

    def write(self, command_str):
        # add term char
        command_str  = command_str.strip()
        command_str += '\n'
        # write
        self.write_bytes(command_str.encode())

    def query(self, command_str):
        self.write(command_str)
        return self.read()
