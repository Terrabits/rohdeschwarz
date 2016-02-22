import datetime
from enum import Enum
import math
import numpy
import uuid


### Enums
class ConnectionMethod(Enum):
    tcpip = 'TCPIP'
    gpib = 'GPIB'
    usb = 'USB'

    def __str__(self):
        return self.value

class SiPrefix(Enum):
    femto = 1.0E-15
    pico = 1.0E-12
    nano = 1.0E-9
    micro = 1.0E-6
    milli = 1.0E-3
    none = 1
    kilo = 1.0E3
    mega = 1.0E6
    giga = 1.0E9
    tera = 1.0E12
    def __float__(self):
        return self.value
    def __str__(self):
        if self == SiPrefix.femto:
            return 'f'
        elif self == SiPrefix.pico:
            return 'p'
        elif self == SiPrefix.nano:
            return 'n'
        elif self == SiPrefix.micro:
            return 'u'
        elif self == SiPrefix.milli:
            return 'm'
        elif self == SiPrefix.kilo:
            return 'K'
        elif self == SiPrefix.mega:
            return 'M'
        elif self == SiPrefix.giga:
            return 'G'
        elif self == SiPrefix.tera:
            return 'T'
        else:
            return ''
    @staticmethod
    def convert(value):
        abs_value = abs(value)
        if abs_value >= 1.0E12:
            return (value * 1.0E-12, SiPrefix.tera)
        elif abs_value >= 1.0E9:
            return (value * 1.0E-9, SiPrefix.giga)
        elif abs_value >= 1.0E6:
            return (value * 1.0E-6, SiPrefix.mega)
        elif abs_value >= 1.0E3:
            return (value * 1.0E-3, SiPrefix.kilo)
        elif abs_value >= 1.0:
            return (value, SiPrefix.none)
        elif abs_value >= 1.0E-3:
            return (value * 1.0E3, SiPrefix.milli)
        elif abs_value >= 1.0E-6:
            return (value * 1.0E6, SiPrefix.micro)
        elif abs_value >= 1.0E-9:
            return (value * 1.0E9, SiPrefix.nano)
        elif abs_value >= 1.0E-12:
            return (value * 1.0E12, SiPrefix.pico)
        else:
            return (value * 1.0E15, SiPrefix.femto)

### Functions
def print_header(file, app_name, app_version):
    #R&S <_appName> Version <_version>
    #(C) 2015 Rohde & Schwarz America
    #
    #Mon Jul 6 15:05:51 2015
    #
    today = datetime.datetime.now()
    file.write("{0} Version {1}\n".format(app_name, app_version))
    file.write("(C) {0} Rohde & Schwarz\n\n".format(today.year))
    file.write(today.strftime('%a %d %b %H:%M:%S %Y\n\n'))

def dB(magnitude):
    """
    Convert complex values or linear magnitude to dB
    Args:
        magnitude (int, float, numpy.float32, numpy, float64, numpy.ndarray)
    Returns:
        Similar type with the value converted to dB
    """
    if isinstance(magnitude, (int, float, numpy.float32, numpy.float64)):
        return 20.0 * math.log10(abs(magnitude))
    elif isinstance(magnitude, numpy.ndarray):
        result = None
        if isinstance(magnitude[0], (numpy.complex64, numpy.complex128)):
            result = numpy.array(abs(magnitude))
        else:
            result = numpy.array(magnitude)
        for i in range(0, len(magnitude)):
            result[i] = dB(result[i])
        return result
    else:
        raise ValueError(0, 'Cannot convert type {0} to dB'.format(type(magnitude)))

def number_of_thrus(port_count):
    f = math.factorial
    if port_count <= 0:
        raise ValueError("number_of_thrus() not defined for port count less than 1")
    elif port_count == 1:
        return 0
    else:
        return f(port_count) / (2*f(port_count-2))

def unique_alphanumeric_string():
    unique_string = str(uuid.uuid4())
    unique_string = unique_string.replace('-', '')
    return unique_string