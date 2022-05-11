from .decode import decode, is_complete
from .encode import encode


class BlockDataMixin:
    def write_block_data(self, data):
        block_data = encode(data)
        # write block then term char
        self.write_bytes(block_data + b'\n')

    def read_block_data(self):
        # transfer until complete
        block_data = self.read_bytes()
        while not is_complete(block_data):
            block_data += self.read_bytes()
        # decode
        return decode(block_data)
