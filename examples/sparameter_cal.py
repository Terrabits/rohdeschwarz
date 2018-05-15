from rohdeschwarz.instruments.vna import Vna

# Connect
vna = Vna()
vna.open_tcp('localhost')

# Preset instrument (optional)
vna.clear_status()
vna.preset()
vna.pause()

# Settings for ch1 calibration
ch1 = vna.channel(1)
ch1.sweep_type = 'lin' # linear freq sweep
ch1.start_frequency_Hz =   1,'GHz'
ch1.stop_frequency_Hz  =   2,'GHz'
ch1.points             = 101
ch1.if_bandwidth_Hz    =   1,'KHz'
ch1.power_dBm          = -10 # dBm

# check for cal unit(s)
assert vna.cal_units

# Calibrate
ports = [1, 2]
ch1.auto_calibrate(ports)
assert not vna.errors
