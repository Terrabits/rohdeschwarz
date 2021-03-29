from   .definitions import Types
import ctypes


class Buffer:
    def __init__(self, size=1024):
        self.size = size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size   = size
        self._buffer = (Types.ViByte * size)()

    @property
    def value(self):
        return self.to_char_p().value

    @value.setter
    def value(self, value):
        self.to_char_p().value = value

    def to_ViBuf(self):
        return self.cast_to(Types.ViBuf)

    def to_ViPChar(self):
        return self.cast_to(Types.ViPChar)

    # helpers
    def cast_to(self, type):
        return ctypes.cast(self._buffer, type)

    def to_char_p(self):
        return self.cast_to(ctypes.c_char_p)
