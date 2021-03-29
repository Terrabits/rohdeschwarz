

class BytesIOMixin:
    def read_bytes(self, read_until_endline=True):
        if not read_until_endline:
            # read once
            return self._read_bytes_no_endline()

        # read until endline
        data = self._read_bytes_no_endline()
        while not data.endswith(self.endline_byte):
            data += self._read_bytes_no_endline()

        # return data without endline
        return data[:-1]

    def write_bytes(self, data, add_endline=True):
        if not add_endline:
            self._write_bytes_no_endline(data)
        else:
            self._write_bytes_no_endline(data + self.endline_byte)

    def query_bytes(self, scpi_bytes):
        self.write_bytes(scpi_bytes, add_endline=True)
        return self.read_bytes(read_until_endline=True)
