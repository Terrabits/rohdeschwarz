from rohdeschwarz.instruments.vna.vnafilesystem import Directory
import re
import pdb

class CalUnit:
    def __init__(self, vna, id=None):
        if not id and vna.cal_units:
            id = vna.cal_units[0]
        self.id  = id
        self.vna = vna

    def select(self):
        scpi = ":SYST:COMM:RDEV:AKAL:ADDR '{0}'"
        scpi = scpi.format(self.id)
        self.vna.write(scpi)

    def __difficult_ports(self):
        self.select()
        current_dir = self.vna.file.directory()
        self.vna.file.cd(Directory.default)
        if not self.vna.file.is_directory('__TEMP__'):
            self.vna.file.mkdir('__TEMP__')
            self.vna.pause()
        self.vna.file.cd('__TEMP__')
        self.vna.file.delete_all('.')
        self.vna.pause()
        self.export_factory_cal(self.vna.file.directory())
        self.vna.pause(10000)
        filenames = self.vna.file.files()
        regex = re.compile(r'CalibrationUnit Open \(P(?P<port>\d+)\)\.s1p', re.IGNORECASE)
        ports = [int(regex.match(f).group('port')) for f in filenames if regex.match(f)]
        self.vna.file.delete_all(self.vna.file.directory())
        self.vna.pause()
        self.vna.file.cd(Directory.default)
        self.vna.file.rmdir('__TEMP__')
        self.vna.pause()
        self.vna.file.cd(current_dir)
        return max(ports)
    def _ports(self):
        if not self.id in self.vna.cal_units:
            raise LookupError("No cal unit with id '{0}'".format(self.id))
        if self.vna.properties.is_zvx():
            # TODO: Make faster?
            return self.__difficult_ports()
            # # This code should be faster theoretically,
            # # but there is a timing bug that requires sleep.... :-(
            # self.vna.is_error()
            # self.vna.clear_status()
            # port = 0
            # while not self.vna.is_error():
            #     port += 1
            #     self.setOpen(port)
            #     time.sleep(5)
            # return port-1
        else:
            # znx
            self.select()
            result = self.vna.query("SYST:COMM:RDEV:AKAL:PORT? ''")
            result = result.strip("'").split(",")
            return int(result[-3])
    ports = property(_ports)

    # TODO
    def _vna_ports_connected(self):
        scpi = 'SENS:CORR:COLL:AUTO:PORT:CONN?'
        result = self.vna.query(scpi)
        result = result.split(",")
        ports = []
        for i in range(0, len(result), 2):
            vna_port  = int(result[i])
            unit_port = int(result[i+1])
            if unit_port != 0:
                ports.append(vna_port)
        return ports
    vna_ports_connected = property(_vna_ports_connected)

    def export_factory_cal(self, path):
        self.select()
        scpi = "MMEM:AKAL:FACT:CONV '{0}'"
        scpi = scpi.format(path)
        self.vna.write(scpi)

    def setOpen(self, port):
        scpi = 'SYST:COMM:AKAL:CONN OPEN,{0}'.format(port)
        self.select()
        self.vna.write(scpi)
    def setShort(self, port):
        scpi = 'SYST:COMM:AKAL:CONN SHOR,{0}'.format(port)
        self.select()
        self.vna.write(scpi)
    def setMatch(self, port):
        scpi = 'SYST:COMM:AKAL:CONN MATC,{0}'.format(port)
        self.select()
        self.vna.write(scpi)
