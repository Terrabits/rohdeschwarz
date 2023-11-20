#!/usr/bin/env python

from   pathlib import Path, PureWindowsPath
from   rohdeschwarz.instruments.vna import Vna, Directory
from   skrf import Network
import sys

if __name__ != '__main__':
    print('Not a library')
    sys.exit(1)

vna = Vna()
vna.open_tcp('127.0.0.1')
vna.open_log('scpi log.txt')

if not vna.cal_units:
    print('No cal unit found')
    sys.exit(1)

# Control cal unit
cal_unit = vna.cal_unit()
cal_unit.setOpen(1)
cal_unit.setShort(1)
cal_unit.setMatch(1)
cal_unit.setThru(1,2)

# Temp dir for cal data
vna.file.cd(Directory.DEFAULT)
temp_dir = PureWindowsPath(vna.file.directory()) / 'CAL_UNIT_DATA'
if vna.file.is_directory(temp_dir):
    vna.file.delete_all(temp_dir)
else:
    vna.file.mkdir(temp_dir)
vna.file.cd(str(temp_dir))

# Export factory cal data files
# from cal unit to VNA,
# download to local computer
dest_dir = Path('.') / 'data'
vna.cal_unit().export_factory_cal(str(temp_dir))
vna.pause(10000)
for i in vna.file.files():
    src  = str(temp_dir / i)
    dest = str(dest_dir / i)
    vna.file.download_file(src, dest)

# Read data.
# Data file naming convention:
open_filename  = 'CalibrationUnit Open (P{0}).s1p'
short_filename = 'CalibrationUnit Short (P{0}).s1p'
match_filename = 'CalibrationUnit Match (P{0}).s1p'
thru_filename  = 'CalibrationUnit Through (P{0}P{1}).s2p'

# Read port 1
# open, short, match
# format is complex (re + j*im)
freq_Hz  = Network(str(dest_dir / open_filename.format(1))).f
p1_open  = [s[0][0] for s in Network(str(dest_dir / open_filename.format(1))).s]
p1_short = [s[0][0] for s in Network(str(dest_dir / short_filename.format(1))).s]
p1_match = [s[0][0] for s in Network(str(dest_dir / match_filename.format(1))).s]

# Read port 1, 2 through,
# if it exists
# format is complex (re + j*im)
p12_thru_path = dest_dir / thru_filename.format(1,2)
if p12_thru_path.exists():
    p12_thru = [s[1][0] for s in Network(str(p12_thru_path)).s]

# cleanup VNA
vna.file.cd('..')
vna.file.delete_all(temp_dir)
vna.file.rmdir(temp_dir)
