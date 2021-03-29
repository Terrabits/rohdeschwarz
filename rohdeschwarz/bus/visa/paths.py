from   ctypes.util import find_library
import platform


WIN_VISA_LIBRARY   = 'visa32'
MACOS_VISA_LIBRARY = 'rsvisa'


def get_visa_path():
    system = platform.system()
    if system == 'Windows':
        # load from path
        return WIN_VISA_LIBRARY
    if system == 'Darwin':
        # load from specific file
        return find_library(MACOS_VISA_LIBRARY)
