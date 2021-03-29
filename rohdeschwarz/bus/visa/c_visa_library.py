from   .paths       import get_visa_path
from   .definitions import FunctionPrototypes
import ctypes


class CVisaLibrary:
    def __init__(self, path=get_visa_path(), load=True):
        self._visa_path = path
        if load:
            self.load()

    # load/unload
    def load(self):
        self._visa_lib  = ctypes.CDLL(self._visa_path)

    def unload(self):
        # TODO
        self._visa_path = None
        self._visa_lib  = None

    @property
    def is_loaded(self):
        return self._visa_lib is not None

    # expose vi functions
    def __getattr__(self, name):
        if not hasattr(self._visa_lib, name):
            raise AttributeError(f'visa has no attribute: {name}')

        attr = getattr(self._visa_lib, name)
        if hasattr(FunctionPrototypes, name):
            prototype     = getattr(FunctionPrototypes, name)
            attr.restype  = prototype['restype']
            attr.argtypes = prototype['argtypes']
        return attr
