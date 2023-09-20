class Segment(object):

    def __init__(self, vna, channel, segment):
        super(Segment, self).__init__()
        self._vna    = vna
        self.channel = channel
        self.index   = segment


    # channel

    @property
    def channel(self):
        return self._channel.index


    @channel.setter
    def channel(self, index):
        self._channel = self._vna.channel(index)


    # on

    @property
    def on(self):
        scpi = ':SENS{0}:SEGM{1}:STAT?'
        scpi = scpi.format(self.channel, self.index)
        return self._vna.query(scpi).strip() == '1'

    @on.setter
    def on(self, on):
        # convert to scpi bool
        on   = '1' if on else '0'

        # set state
        scpi = ':SENS{0}:SEGM{1}:STAT {2}'
        scpi = scpi.format(self.channel, self.index, on)
        self._vna.write(scpi)


    # start frequency

    @property
    def start_frequency_Hz(self):
        scpi    = ':SENS{0}:SEGM{1}:FREQ:STAR?'
        scpi    = scpi.format(self.channel, self.index)
        freq_Hz = self._vna.query(scpi)
        return float(freq_Hz)


    @start_frequency_Hz.setter
    def start_frequency_Hz(self, frequency_Hz):
        # with units?
        try:
            if len(frequency_Hz) == 2:
                frequency_Hz = ' '.join(frequency_Hz)
        except TypeError:
            pass

        scpi = ':SENS{0}:SEGM{1}:FREQ:STAR {2}'
        scpi = scpi.format(self.channel, self.index, frequency_Hz)
        self._vna.write(scpi)


    # stop frequency

    @property
    def stop_frequency_Hz(self):
        scpi    = ':SENS{0}:SEGM{1}:FREQ:STOP?'
        scpi    = scpi.format(self.channel, self.index)
        freq_Hz = self._vna.query(scpi)
        return float(freq_Hz)


    @stop_frequency_Hz.setter
    def stop_frequency_Hz(self, frequency_Hz):
        # with units?
        try:
            if len(frequency_Hz) == 2:
                frequency_Hz = ' '.join(frequency_Hz)
        except TypeError:
            pass

        scpi = ':SENS{0}:SEGM{1}:FREQ:STOP {2}'
        scpi = scpi.format(self.channel, self.index, frequency_Hz)
        self._vna.write(scpi)


    # points

    @property
    def points(self):
        scpi   = ':SENS{0}:SEGM{1}:SWE:POIN?'
        scpi   = scpi.format(self.channel, self.index)
        points = self._vna.query(scpi)
        return int(points)


    @points.setter
    def points(self, points):
        scpi = ':SENS{0}:SEGM{1}:SWE:POIN {2}'
        scpi = scpi.format(self.channel, self.index, points)
        self._vna.write(scpi)


    # if bandwidth

    @property
    def if_bandwidth_Hz(self):
        scpi    = ':SENS{0}:SEGM{1}:BWID?'
        scpi    = scpi.format(self.channel, self.index)
        bandwidth_Hz = self._vna.query(scpi)
        return float(bandwidth_Hz)


    @if_bandwidth_Hz.setter
    def if_bandwidth_Hz(self, if_bandwidth_Hz):
        # with units?
        try:
            if len(if_bandwidth_Hz) == 2:
                if_bandwidth_Hz = ' '.join(if_bandwidth_Hz)
        except TypeError:
            pass

        scpi = ':SENS{0}:SEGM{1}:BWID {2}'
        scpi = scpi.format(self.channel, self.index, if_bandwidth_Hz)
        self._vna.write(scpi)


    # power

    @property
    def power_dBm(self):
        scpi      = ':SENS{0}:SEGM{1}:POW?'
        scpi      = scpi.format(self.channel, self.index)
        power_dBm = self._vna.query(scpi)
        return float(power_dBm)


    @power_dBm.setter
    def power_dBm(self, power_dBm):
        scpi = ':SENS{0}:SEGM{1}:POW {2}'
        scpi = scpi.format(self.channel, self.index, power_dBm)
        self._vna.write(scpi)
