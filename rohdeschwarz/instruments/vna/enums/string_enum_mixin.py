from enum import Enum


class StringEnumMixin(str, Enum):

    def __str__(self):
        return self.value
