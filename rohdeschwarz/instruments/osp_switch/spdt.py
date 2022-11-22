from enum import IntEnum


class Spdt(IntEnum):
    """single-pole, double-throw switch state"""
    nc = 0,
    no = 1

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_str(value_str):
        
