from enum import Enum


class TriggerSource(Enum):
    pass


class Trigger:
    """
    Channel trigger settings
    """


    # life cycle

    def __init__(self, vna, channel_index):
        """
        constructor

        Arguments:
        vna           -- `Vna` object
        channel_index -- `int`; channel index
        """
        self._vna     = vna
        self._channel = channel_index


    # triggered sequence

    @property
    def sequence(self):
        """trigger sequence

        Determines the measurement or measurement sequence
        initiated by the trigger.

        Type:
            str
        Values:
        - `SWEEP`
        - `SEGMENT`
        - `POINT`
        - `PPOINT` (partial point)
        """
        scpi = f':TRIG{self._channel}:LINK?'
        return self._vna.query(scpi).strip().strip("'")


    @sequence.setter
    def sequence(self, sequence):
        scpi = f":TRIG{self._channel}:LINK '{sequence}'"
        self._vna.write(scpi)


    # trigger source

    @property
    def source(self):
        """trigger source

        Type:
            str
        Values:
        - "IMM"  (immediate)
        - "EXT"  (exernal)
        - "TIM"  (timer)
        - "MAN"  (manual)
        - "PGEN" (pulse generator)
        - "MULT" (multiple trigger sources)
        """
        scpi = f':TRIG{self._channel}:SOUR?'
        return self._vna.query(scpi).strip()


    @source.setter
    def source(self, source):
        scpi = f':TRIG{self._channel}:SOUR {source}'
        self._vna.write(scpi)



    # external trigger source

    @property
    def external_source(self):
        """
        external trigger source(str)
        values: ``, ``, ``, ``
        """
        scpi = f'TRIG{self._channel}:EINP?'
        return self._vna.query(scpi).strip()


    @external_source.setter
    def external_source(self, source):
        """set external trigger source """
        scpi = f'TRIG{self._channel}:EINP {source}'
        self._vna.write(scpi)


    # trigger slope

    def _slope(self):
        """get trigger slope """
        scpi = f':TRIG{self._channel}:SLOP?'
        return self._vna.query(scpi).strip()


    def _set_slope(self, slope):
        """set trigger slope """
        scpi = f':TRIG{self._channel}:SLOP {slope}'
        self._vna.write(scpi)


    """trigger slope """
    slope = property(_slope, _set_slope)
