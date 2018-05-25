#!/usr/bin/env bash

from rohdeschwarz.instruments.vna import Vna

vna = Vna()
vna.open_tcp('localhost')

# Optional preset
vna.clear_status()
vna.preset()
vna.pause()

# settings for power cal
ch1 = vna.channel(1)
ch1.sweep_type = 'pow' # power sweep
ch1.start_power_dBm = -30
ch1.stop_power_dBm  = -10
ch1.points          = 101
ch1.if_bandwidth_Hz = 1,'KHz'

# Check for power sensor(s)
assert vna.power_sensors

# Perform power cal
source_port   = 1
receiver_port = 2
print('Connect port {0} to power sensor'.format(source_port))
input('Press enter to continue')
ch1.source_power_cal(source_port, sweeps=10, tolerance=0.1)
assert not vna.errors

print('Connect port {1} to port {2} (thru)'.format(source_port, receiver_port))
input('Press enter to continue')
ch1.receiver_power_cal(receiver_port, source_port)
assert not vna.errors
