from enum import Enum
import sys

class EmulationMode(Enum):
    pna = 'PNA'
    ena = 'ENA'
    hp_8510 = 'HP8510'
    hp_8530 = 'HP8530'
    hp_8720 = 'HP8720'
    hp_8753 = 'HP8753'
    hp_8714 = 'HP8714'
    zvr = 'ZVR'
    zvabt = 'ZVABT'
    off = 'SCPI'
    def __bool__(self):
        return not self == EmulationMode.off
    def __str__(self):
        return self.value

class PortPowerLimits(object):
        def __init__(self, vna):
            super(PortPowerLimits, self).__init__()
            self._vna = vna

        def __getitem__(self, index):
            scpi = ':SOUR:POW{0}:LLIM?'
            scpi = scpi.format(index+1)
            limit = self._vna.query(scpi).strip()
            limit = limit == "1"
            if not limit:
                return None
            scpi = ':SOUR:POW{0}:LLIM:VAL?'
            scpi = scpi.format(index+1)
            result = self._vna.query(scpi).strip()
            return float(result)
        def __setitem__(self, index, value):
            if isinstance(value, bool) and value == False:
                value = None
            if isinstance(value, (int, float)):
                scpi = ':SOUR:POW{0}:LLIM 1'
                scpi = scpi.format(index+1)
                self._vna.write(scpi)
                scpi = ':SOUR:POW{0}:LLIM:VAL {1}'
                scpi = scpi.format(index+1, value)
                self._vna.write(scpi)
            elif not value:
                scpi = ':SOUR:POW{0}:LLIM 0'
                scpi = scpi.format(index+1)
                self._vna.write(scpi)
        def __len__(self):
            return self._vna.properties.physical_ports
        def __bool__(self):
            value = isinstance(self.__getitem__(0), float)
            ports = self.__len__()
            for i in range(1, ports):
                if value != isinstance(self.__getitem__(i), float):
                    raise ValueError
            return value
        def __float__(self):
            value = self.__getitem__(0)
            if not isinstance(value, float):
                raise ValueError
            ports = self.__len__()
            for i in range(1, ports):
                next_value = self.__getitem__(i)
                if not isinstance(next_value, float):
                    raise ValueError
                if value != self.__getitem__(i):
                    raise ValueError
            return value
        def __str__(self):
            try:
                single_value = self.__float__()
                return str(single_value)
            except:
                pass
            try:
                value = self.__bool__()
                if not value:
                    return str(value)
            except:
                pass
            values = []
            ports = self.__len__()
            for i in range(0, ports):
                values.append(self.__getitem__(i))
            return str(values)
        def __repr__(self):
            return self.__str__()

class Settings(object):
    def __init__(self, vna):
        self._vna = vna

    def _data_format(self):
            return self._vna.query(':FORM?').strip()
    def _set_data_format(self, data_format):
            scpi = ":FORM {0}"
            scpi = scpi.format(data_format)
            self._vna.write(scpi)
    data_format = property(_data_format, _set_data_format)

    def _ascii_data_format(self):
        result = self._vna.query(':FORM?').strip()
        return result == 'ASC,0'
    def _set_ascii_data_format(self, value):
        if value:
            self._vna.write(':FORM ASC')
    ascii_data_format = property(_ascii_data_format, _set_ascii_data_format)

    def _binary_32_bit_data_format(self):
        result = self._vna.query(':FORM?').strip()
        return result == 'REAL,32'
    def _set_binary_32_bit_data_format(self, value):
        if value:
            self._vna.write(':FORM REAL,32')
    binary_32_bit_data_format = property(_binary_32_bit_data_format, _set_binary_32_bit_data_format)

    def _binary_64_bit_data_format(self):
        result = self._vna.query(':FORM?').strip()
        return result == 'REAL,64'
    def _set_binary_64_bit_data_format(self, value):
        if value:
            self._vna.write(':FORM REAL,64')
    binary_64_bit_data_format = property(_binary_64_bit_data_format, _set_binary_64_bit_data_format)

    def _big_endian(self):
        scpi = ':FORM:BORD?'
        result = self._vna.query(scpi).strip().upper()
        return result == 'NORM'
    def _set_big_endian(self, is_big_endian):
        # Date: June 2021
        # ZNL(E) does not support this command
        # Assumes SWAP
        model = str(self._vna.properties.model)
        if model == 'ZNL' or model == 'ZNLE':
            if is_big_endian:
                raise Exception('{0} does not support big endian'.format(model))
            # no-op
            return

        # set
        scpi_value = 'NORM' if is_big_endian else 'SWAP'
        scpi       = 'FORM:BORD {0}'.format(scpi_value)
        self._vna.write(scpi)
    big_endian = property(_big_endian, _set_big_endian)

    def _little_endian(self):
        return not self.big_endian
    def _set_little_endian(self, is_little_endian):
        self.big_endian = not is_little_endian
    little_endian = property(_little_endian, _set_little_endian)


    # byte order

    @property
    def byte_order(self):
        """
        byte order

        Value:
        `str`, "NORM" (big-endian) or "SWAP" (little-endian)
        """
        return self._vna.query(':FORM:BORD?').strip()


    @byte_order.setter
    def byte_order(self, byte_order):
        scpi = f':FORM:BORD {byte_order}'
        self._vna.write(scpi)



    def _emulation_mode(self):
        # ':SYST:LANG?'
        result = self._vna.query(':SYST:LANG?').strip().strip("'").upper()
        return EmulationMode(result)
    def _set_emulation_mode(self, value):
        if not value:
            value = EmulationMode.off
        scpi = ":SYST:LANG '{0}'"
        scpi = scpi.format(value)
        self._vna.write(scpi)
    emulation_mode = property(_emulation_mode, _set_emulation_mode)

    def _display(self):
        scpi = ':SYST:DISP:UPD?'
        result = self._vna.query(scpi).strip()
        return result == "1"
    def _set_display(self, value):
        if value:
            self._vna.write(':SYST:DISP:UPD ON')
        else:
            self._vna.write(':SYST:DISP:UPD OFF')
    display = property(_display, _set_display)

    def update_display(self):
        self._vna.write(':SYST:DISP:UPD ONCE')

    def _display_errors(self):
        scpi = ':SYST:ERR:DISP?'
        result = self._vna.query(scpi).strip()
        return result == "1"
    def _set_display_errors(self, value):
        if value:
            self._vna.write(':SYST:ERR:DISP 1')
        else:
            self._vna.write(':SYST:ERR:DISP 0')
    display_errors = property(_display_errors, _set_display_errors)

    def _user_preset(self):
        preset_on = self._vna.query(':SYST:PRES:USER?')
        preset_on = preset_on.strip() == "1"
        if not preset_on:
            return None
        else:
            result = self._vna.query(':SYST:PRES:USER:NAME?')
            result = result.strip().strip("'")
            return result
    def _set_user_preset(self, value):
        if not value:
            self._vna.write(':SYST:PRES:USER 0')
        else:
            scpi = ":SYST:PRES:USER:NAME '{0}'"
            scpi = scpi.format(value)
            self._vna.write(scpi)
            self._vna.write(':SYST:PRES:USER 1')
    user_preset = property(_user_preset, _set_user_preset)

    def _user_preset_remotely(self):
        return self._vna.query(':SYST:PRES:REM?').strip() == "1"
    def _set_user_preset_remotely(self, value):
        if value:
            self._vna.write(':SYST:PRES:REM 1')
        else:
            self._vna.write(':SYST:PRES:REM 0')
    user_preset_remotely = property(_user_preset_remotely, _set_user_preset_remotely)

    def _use_cal_group_on_preset(self):
        if self._vna.properties.is_zvx():
            message = 'ZVx does not support cal group on preset!\n'
            sys.stderr.write(message)
            if self._vna.log and not self._vna.log.closed:
                self._vna.log.write(message)
                self._vna.log.write('\n')
            return None
        result = self._vna.query(':SYST:PRES:USER:CAL?')
        result = result.strip().strip("'")
        if len(result) == 0:
            return None
        else:
            return result
    def _set_use_cal_group_on_preset(self, value):
        if self._vna.properties.is_zvx():
            message = 'ZVx does not support cal group on preset!\n'
            sys.stderr.write(message)
            if self._vna.log and not self._vna.log.closed:
                self._vna.log.write(message)
                self._vna.log.write('\n')
            return
        if not value:
            value = ''
        scpi = ":SYST:PRES:USER:CAL '{0}'"
        scpi = scpi.format(value)
        self._vna.write(scpi)
    use_cal_group_on_preset = property(_use_cal_group_on_preset, _set_use_cal_group_on_preset)

    def _output_power_on(self):
        result = self._vna.query(':OUTP?')
        result = result.strip()
        return result == "1"
    def _set_output_power_on(self, value):
        if value:
            self._vna.write(':OUTP 1')
        else:
            self._vna.write(':OUTP 0')
    output_power_on = property(_output_power_on, _set_output_power_on)

    def _dynamic_if_bandwidth(self):
        if self._vna.properties.is_znx():
            message = 'ZNx does not support dynamic if bandwidth!\n'
            sys.stderr.write(message)
            if self._vna.log and not self._vna.log.closed:
                self._vna.log.write(message)
                self._vna.log.write('\n')
            return
        result = self._vna.query(':BAND:DRED?')
        result = result.strip()
        return result == "1"
    def _set_dynamic_if_bandwidth(self, value):
        if self._vna.properties.is_znx():
            message = 'ZNx does not support dynamic if bandwidth!\n'
            sys.stderr.write(message)
            if self._vna.log and not self._vna.log.closed:
                self._vna.log.write(message)
                self._vna.log.write('\n')
            return
        if value:
            self._vna.write(':BAND:DRED 1')
        else:
            self._vna.write(':BAND:DRED 0')
    dynamic_if_bandwidth = property(_dynamic_if_bandwidth, _set_dynamic_if_bandwidth)

    def _reduce_cal_unit_power(self):
        scpi = ':SYST:COMM:RDEV:AKAL:PRED'
        result = self._vna.query(scpi)
        return result.strip() == "1"
    def _set_reduce_cal_unit_power(self, value):
        if value:
            self._vna.write(':SYST:COMM:RDEV:AKAL:PRED 1')
        else:
            self._vna.write(':SYST:COMM:RDEV:AKAL:PRED 0')
    reduce_cal_unit_power = property(_reduce_cal_unit_power, _set_reduce_cal_unit_power)

    def _log_scpi_commands(self):
        scpi = ':SYST:LOGG:REM?'
        result = self._vna.query(scpi)
        return result.strip() == "1"
    def _set_log_scpi_commands(self, value):
        if value:
            self._vna.write(':SYST:LOGG:REM 1')
        else:
            self._vna.write(':SYST:LOGG:REM 0')
    log_scpi_commands = property(_log_scpi_commands, _set_log_scpi_commands)

    def _port_power_limit_class(self):
        return PortPowerLimits(self._vna)
    def _set_port_power_limit(self, power):
        limits = PortPowerLimits(self._vna)
        ports = len(limits)
        for i in range(0, ports):
            limits[i] = power
    port_power_limit_dBm = property(_port_power_limit_class, _set_port_power_limit)
