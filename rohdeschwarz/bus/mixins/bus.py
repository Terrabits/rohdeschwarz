from .bytes_io  import BytesIOMixin
from .string_io import StringIOMixin


class BusMixin(StringIOMixin, BytesIOMixin):
    pass
