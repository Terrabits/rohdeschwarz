import datetime
from enum import Enum


### Enums
class ConnectionMethod(Enum):
    tcpip = 'TCPIP'
    gpib = 'GPIB'
    usb = 'USB'

    def __str__(self):
        return self.value

class SiPrefix(Enum):
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
        if self == SiPrefix.pico:
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
