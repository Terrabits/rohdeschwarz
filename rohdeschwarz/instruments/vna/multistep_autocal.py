from rohdeschwarz.general import number_of_thrus

class MultistepAutocal:
    def __init__(self, vna, channel, cal_unit=''):
        self.vna      = vna
        self.channel  = channel
        self.ports = []
        if not cal_unit:
            cal_unit  = vna.cal_units[0]
        self.cal_unit = vna.cal_unit(cal_unit)

    def start(self, ports):
        self.ports = ports
        self.cal_unit.select()
        # cal type: full n port
        scpi = "SENS{0}:CORR:COLL:AUTO:CONF FNP, ''"
        scpi = scpi.format(self.channel.index)
        self.vna.write(scpi)
        # set ports
        scpi = "SENS{0}:CORR:COLL:AUTO:ASS:DEF:TPOR:DEF"
        scpi = scpi.format(self.channel.index, ",".join(ports))
        self.vna.write(scpi)

    def _steps(self):
        scpi = 'SENS{0}:CORR:COLL:AUTO:ASS:COUN?'
        scpi = scpi.format(self.channel.index)
        num_steps = int(self.vna.query(scpi).strip())
        steps = []
        for i in range(1,num_steps):
            scpi = 'SENS{0}:CORR:COLL:AUTO:ASS:DEF:TPOR?'
            scpi = scpi.format(self.channel.index)
            step = self.vna.query(scpi).strip().split(",")
            step = [int(port) for port in step]
            steps.append(step)
        return steps
    steps = property(_steps)

    def perform_step(self, i):
        scpi = 'SENS{0}:]CORR:COLL:AUTO:ASS{1}:ACQ'
        scpi = scpi.format(self.channel.index, i)

        port_count = len(self.steps[i])
        number_of_sweeps = 3 * port_count + number_of_thrus(port_count)
        timeout_ms = number_of_sweeps * (10 * self.channel.total_sweep_time_ms + 10000) + 5000

        self.vna.write(scpi)
        self.vna.pause(timeout_ms)

    def apply(self):
        scpi = 'SENS{0}:CORR:COLL:AUTO:SAVE'
        scpi = scpi.format(self.channel.index)
        self.vna.write(scpi)
        self.vna.pause(30*1000) # 30 seconds
