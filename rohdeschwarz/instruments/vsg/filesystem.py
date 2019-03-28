import csv
import os
from   pathlib import Path, PurePosixPath

class FileSystem(object):
    def __init__(self, vsg):
        self._vsg = vsg
    def ls(self):
        return [i[0] for i in self._mmem_cat()]
    def files(self):
        return [i[0] for i in self._mmem_cat() if i[1] != 'DIR']
    def directories(self):
        return [i[0] for i in self._mmem_cat() if i[1] == 'DIR']
    def cd(self, path=None):
        if not path:
            return self._vsg.query('MMEM:CDIR?').replace('"', '').strip()
        else:
            self._vsg.write("MMEM:CDIR '{}'".format(path))

    def rm(self, filename):
        scpi = "MMEM:DEL '{}'".format(filename)
        self._vsg.write(scpi)
    def mkdir(self, path):
        scpi = "MMEM:MDIR '{}'".format(path)
        self._vsg.write(scpi)
    def rmdir(self, path):
        scpi = "MMEM:RDIR '{}'".format(path)
        self._vsg.write(scpi)

    def upload_file(self, local_filename, remote_filename=None):
        assert os.path.isfile(local_filename)
        assert os.access(local_filename, os.R_OK)
        if not remote_filename:
            remote_filename = Path(local_filename).name
        scpi = "MMEM:DATA '{}',".format(remote_filename)
        self._vsg.write_raw_no_end(scpi.encode())
        self._vsg.write_block_data_from_file(local_filename)
    def download_file(self, remote_filename, local_filename=None):
        if not local_filename:
            local_filename = PurePosixPath(remote_filename).name
        scpi = "MMEM:DATA? '{}'".format(remote_filename)
        self._vsg.write(scpi)
        self._vsg.read_block_data_to_file(local_filename)
        
    def _mmem_cat(self):
        response = self._vsg.query('MMEM:CAT?').strip()
        response = list(csv.reader([response], delimiter=',', quotechar='"'))[0]
        used_B   = int(response[0])
        free_B   = int(response[1])
        return [i.split(',') for i in response[4:]]
