import sys
from pyvisa.errors import VisaIOError
from rohdeschwarz import *
from rohdeschwarz.instruments.vna import *

vna = Vna()
try:
    vna.open()
except VisaIOError:
    sys.stderr.write('Instrument not found!')
    sys.exit("Instrument not found!")
if not vna.connected():
    sys.stderr.write('Instrument not found!')
    sys.exit("Instrument not found!")

log_filename = 'Test Log.txt'
vna.open_log(log_filename)
print_header(vna.log, "R&S Application", "1.0")
vna.print_info()

vna.is_error()
vna.clear_status()
vna.preset()

vna.channel().save_measurement('C:\\Users\\lalic\\Documents\\Python\\Test', \
                               [1,2,3,4], \
                               'LOGP')

