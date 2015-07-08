import sys
from pyvisa.errors import VisaIOError
from rohdeschwarz import *
from rohdeschwarz.instruments.vna import *

vna = Vna()
try:
    vna.open()
except VisaIOError:
    print('Instrument not found!')
    sys.exit("Instrument not found!")

if not vna.connected():
    print('Instrument not found!')
    sys.exit("Instrument not found!")

vna.log = open('Test Log.txt', 'w')

print_header(vna.log, "R&S Application", "1.0")
vna.print_info()

vna.is_error()
vna.clear_status()

