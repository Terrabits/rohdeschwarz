from   ctypes.util import find_library
import platform


WIN_VISA_LIBRARY = 'visa32'
RS_VISA_LIBRARY  = 'rsvisa'


def get_visa_path():
    if platform.system() == 'Windows':
        return WIN_VISA_LIBRARY
    # else
    return find_library(RS_VISA_LIBRARY)
