from rohdeschwarz.instruments.vna import Vna

# Connect
vna = Vna()
vna.open_tcp('127.0.0.1')

# Calibrate channel 1 ports 1, 2
# using automatic cal unit
index = 1
ports = [1, 2]
vna.channel(index).auto_calibrate(ports)
