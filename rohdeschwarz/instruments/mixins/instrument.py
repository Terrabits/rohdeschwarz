from .block_io        import BlockIOMixin
from .bytes_io        import BytesIOMixin
from .errors          import ErrorsMixin
from .general_scpi    import GeneralScpiMixin
from .local_remote    import LocalRemoteMixin
from .log             import LogMixin
from .string_io       import StringIOMixin
from .synchronization import SynchronizationMixin
from .timeout         import TimeoutMixin
from .vector_io       import VectorIOMixin


MIXINS = [BlockIOMixin,
          BytesIOMixin,
          ErrorsMixin,
          GeneralScpiMixin,
          LocalRemoteMixin,
          LogMixin,
          StringIOMixin,
          SynchronizationMixin,
          TimeoutMixin,
          VectorIOMixin]


def has_delete(Mixin):
    return hasattr(Mixin, '__del__')


class InstrumentMixin(*MIXINS):
    def __init__(self, *args, **kwargs):
        for Mixin in MIXINS:
            Mixin.__init__(self, *args, **kwargs)

    def __del__(self):
        for Mixin in MIXINS:
            if has_delete(Mixin):
                Mixin.__del__(self)
