from enum import IntEnum

class Spdt(IntEnum):
    nc = 0,
    no = 1
    def __str__(self):
        return str(self.value)

class Sp6t(IntEnum):
    t1 = 1,
    t2 = 2,
    t3 = 3,
    t4 = 4,
    t5 = 5,
    t6 = 6
    def __str__(self):
        return str(self.value)
