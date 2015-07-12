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

# vna.file.download_file('C:\\Users\\lalic\\Documents\\Qt\\RsaToolbox\\To do.txt', 'C:\\Users\\lalic\\Documents\\Python\\rohdeschwarz\\tests\\To do.txt')
# vna.file.upload_file('C:\\Users\\lalic\\Documents\\Python\\rohdeschwarz\\tests\\test.py', 'C:\\Users\\lalic\\Documents\\Python\\rohdeschwarz\\tests\\test_copy.txt')

