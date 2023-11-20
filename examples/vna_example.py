"""
Python rohdeschwarz VNA example
"""

import sys

if __name__ != "__main__":
    print("'{0}'\nis a script. Do not import!".format(__file__))
    print('Exiting...')
    sys.exit()

from rohdeschwarz import *
from rohdeschwarz.instruments.vna import *

vna = Vna()

# Open connection via pyvisa
### vna.open('TCPIP|GPIB|USB', 'address')

# Open connection via pyvisa with
# defaults: TCPIP, address 127.0.0.1
### vna.open()

# Open TCP socket connection (no VISA)
# with defaults:
# address '127.0.0.1', port 5025
vna.open_tcp()

# Open TCP socket connection (no VISA)
### vna.open_tcp('address', 'port')

# Create SCPI command log
vna.open_log('SCPI Command Log.txt')

# Print headers:
print_header(vna.log, "VNA Example", "0.0.1")
vna.print_info()

# Send SCPI commands manually:
vna.write('*IDN?')
vna.read()
vna.query('*IDN?')

# Get id string:
vna.id_string()

# Test if Rohde & Schwarz instrument:
vna.is_rohde_schwarz()

# VNA basics

# Preset the instrument:
vna.preset()

# Pause until previous command
# completes:
vna.pause()

# Pause using a custom timeout (ms):
### vna.pause(10000)

# Query error
# returns bool
vna.is_error()

# Get errors
# list of tuples of format:
# [(error_code, 'Error string'),...]
vna.errors

# Clear status/errors
vna.clear_status()

# Properties
vna.properties.model
vna.properties.serial_number
vna.properties.firmware_version
vna.properties.options_list

vna.properties.physical_ports
vna.properties.maximum_frequency_Hz
vna.properties.minimum_frequency_Hz
vna.properties.maximum_power_dBm
vna.properties.minimum_power_dBm
vna.properties.maximum_points

# Global settings

# Turn off emulation mode:
vna.settings.emulation_mode = None

# Set emulation mode to HP 8753:
### vna.settings.emulation_mode = EmulationMode.hp_8753
# - OR - if you know the SCPI command parameter:
### vna.settings.emulation_mode = 'HP8753'

# Turn the display on (continuously)
# while remote:
vna.settings.display = True

# Update display once only
### vna.settings.update_display()

# Turn on RF power:
vna.settings.output_power_on = True

# Display errors:
vna.settings.display_errors = True

# Turn off port power limits:
vna.settings.port_power_limit_dBm = None

# Set port power limit on port 1 only:
### vna.settings.port_power_limit_dBm[1] = -10

# Set port power limits by list:
### vna.settings.port_power_limit_dBm = [None, None, -10, None]

# Set data format to ASCII:
vna.settings.ascii_data_format = True

# Set 64 bit binary data transfer format,
# byte order to big-endian
### vna.settings.binary_64_bit_data_format = True
### vna.settings.big_endian = True

# Set a user preset
### vna.settings.user_preset = 'my_preset'

# Apply user preset on remote preset
# vna.preset() or '*RST':
vna.settings.user_preset_remotely = True


# VNA File system

# Get current directory
vna.file.directory()

# Change current directory
vna.file.cd(Directory.DEFAULT)

# Change current directory manually:
### vna.file.cd('C:\\Users\\Public\\Documents\\Rohde-Schwarz\\Vna')

# Get directories in current directory
vna.file.directories()

# Get files in current directory
vna.file.files()

# Test for existence:
### vna.file.is_file('/path/to/file')
### vna.file.is_directory('/path/to/directory')

# Move file
### vna.file.move('/path/to/source', '/path/to/destination')

# Copy file
### vna.file.copy('/path/to/source', '/path/to/destination')

# Delete file
### vna.file.delete('/path/to/file')

# Make new directory:
### vna.file.mkdir('My New Directory')

# Remove new directory
### vna.file.rmdir('My New Directory')

# Upload file onto instrument:
### vna.file.upload_file('/path/to/local/source_file', '/path/to/remote/destination_file')

# Download file from instrument
### vna.file.download_file('/path/to/remote/source_file', '/path/to/local/destination_file')



# Total availabel test ports
# (including matrix)
vna.test_ports

# Channels (list)
vna.channels

# Create channel:
new_channel = vna.create_channel()

# Create channel with a specific index:
vna.create_channel(10)

# Create a list of channels
vna.channels = list(range(1,11))

# Delete a specific channel:
vna.delete_channel(10)

# Remove all channels except 1:
vna.channels = [1]

# Channel 1 sweep type:
vna.channel(1).sweep_type = SweepType.LINEAR
# - OR - if you know the SCPI parameter:
### vna.channel(1).sweep_type = 'LIN'

# Set Channel 1 sweep parameters:
vna.channel(1).start_frequency_Hz = 1, 'GHz'
vna.channel(1).stop_frequency_Hz = 8, 'GHz'
vna.channel(1).points = 201

# Get frequencies as numpy.ndarray
# of Float64
vna.channel(1).frequencies_Hz

# Set IF BF, power level
vna.channel(1).if_bandwidth_Hz = 1, 'KHz'
vna.channel(1).power_dBm = 0

# Set averaging
vna.channel(1).averages = 10

# Set manual sweep:
vna.channel(1).manual_sweep = True

# Set sweep count to number of averages
vna.channel(1).sweep_count = vna.channel(1).averages

# Turn averaging off
vna.channel(1).averages = None

# Set sweep count back to 1
vna.channel(1).sweep_count = 1

# Set continuous sweep mode
vna.channel(1).manual_sweep = False
# - OR -
### vna.channel(1).continuous_sweep = True

# Measure S-Parameters for [ports]
# Sweep timing handled automatically
# Returns result:
# 3-Dimensional numpy.ndarray:
# [freq_point][output_port-1][input_port-1]
y = vna.channel(1).measure([1,2])

# Save S-Parameters for [ports]
# to touchstone file
# Default format: Re/Im
# If missing, file extension (.sNp)
# is added automatically
### vna.channel(1).save_measurement('/path/to/remote/snp_file', [1,2,])

# Save S-Parameters to touchstone file
# with dB, degrees format:
### vna.channel(1).save_measurement('/path/to/remote/snp_file', [1,2], TouchstoneFormat.DB_DEGREES)


# Diagrams

# List of all diagrams:
vna.diagrams

# Create list of 10 diagrams:
vna.diagrams = list(range(1,11))

# Remove all diagrams except 1, 2:
vna.diagrams = [1, 2]

# Set title of diagram 2
vna.diagram(2).title = 'My Diagram'

# Traces

# List of all traces:
vna.traces

# Create trace with default parameters:
# 'TrcN' where N is next available index
# channel 1
# parameter 'S11'
trace_name = vna.create_trace()

# Delete trace:
vna.delete_trace(trace_name)

# Create trace with specific
# channel, S-Parameter:
trace_name = vna.create_trace(None, 1, 'S21')

# Delete trace:
vna.delete_trace(trace_name)

# Create trace with specific
# Name, channel, parameter:
vna.create_trace('My_Trace', 1, 'S11')

# Assign 'My_Trace' to diagram 2:
vna.trace('My_Trace').diagram = 2

# Change 'My_Trace' to 'S22':
vna.trace('My_Trace').parameter = 'S22'

# Set Format to dB:
vna.trace('My_Trace').format = TraceFormat.MAGNITUDE_DB
# - OR - if you know the SCPI parameter:
### vna.trace('My_Trace').format = 'MLOG'

# Measure formatted trace data
# x = Hz, y = dB:
x, y = vna.trace('My_Trace').measure_formatted_data()

# Measure complex trace data
# y is numpy.ndarray of complex128
x, y = vna.trace('My_Trace').measure_complex_data()

# Save formatted trace data to csv file:
### vna.trace('My_Trace').save_data('/path/to/remote/file.csv')

# Save complex trace data
# Default format is Re/Im:
### vna.trace('My_Trace').save_complex_data('/path/to/remote/file.csv', SaveDataFormat.DB_DEGREES)

# Close Log
vna.close_log()

# Close connection
vna.close()
