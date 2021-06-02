from rohdeschwarz.block_data import parse_header, to_block_data


class BlockIOMixin:
    def read_block_data(self):
        # first read should include header
        data_length, data = parse_header(self.read_bytes(read_until_endline=False))

        # read until data plus endline received
        data_length_plus_endline = data_length + 1
        while len(data) < data_length_plus_endline:
            data += self.read_bytes(read_until_endline=False)

        # remove endline
        data = data[:data_length]

        return data_length, data

    def write_block_data(self, data):
        self.write_bytes(to_block_data(data))
