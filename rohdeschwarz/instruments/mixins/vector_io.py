import numpy as np


class VectorIOMixin:
    def read_64_bit_vector(self):
        return self.read_vector('float64')

    def read_64_bit_complex_vector(self):
        return self.read_vector('complex128')

    def write_vector(self, data):
        data = np.array(data)
        self.write_block_data(data.tobytes())


    # helpers
    def read_vector(self, type='float64'):
        data_length, data = self.read_block_data()
        return np.frombuffer(data, type)
