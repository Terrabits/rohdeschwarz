from enum import Enum
import pathlib

class Directory(Enum):
    default = 'DEF'
    embed = '.\\Embedding'
    deembed = '.\\Deembedding'
    cal_group = '.\\Calibration\\Data'
    cal_kit = '.\\Calibration\\Kits'
    external_tools = '.\\External Tools'
    recall_sets = '.\\RecallSets'
    traces = '.\\Traces'

    def __str__(self):
        return self.value


class VnaFileSystem:
    def __init__(self, vna):
        self._vna = vna

    def cd(self, path):
        if isinstance(path, Directory):
            if path == Directory.default:
                self._vna.write(":MMEM:CDIR DEF")
            else:
                self.cd(Directory.default)
                scpi = ":MMEM:CDIR '{0}'"
                self._vna.write(scpi.format(path))
        else:
            scpi = ":MMEM:CDIR '{0}'"
            self._vna.write(scpi.format(path))

    def is_file(self, path):
        path = pathlib.PureWindowsPath(path)
        location = str(path.parent).replace("/", "\\")
        name = path.name
        original_dir = self.directory()
        if location != ".":
            self.cd(location)
        files = self.files()
        for f in files:
            if f[0].upper() == name.upper():
                if location != ".":
                    self.cd(original_dir)
                return True
        # Else
        if location != ".":
            self.cd(original_dir)
        return False

    def is_directory(self, path):
        path = pathlib.PureWindowsPath(path)
        location = str(path.parent).replace("/", "\\")
        name = path.name
        original_dir = self.directory()
        if location != ".":
            self.cd(location)
        directories= self.directories()
        for d in directories:
            if d.upper() == name.upper():
                if location != ".":
                    self.cd(original_dir)
                return True
        # Else
        if location != ".":
            self.cd(original_dir)
        return False

    def directory(self):
        scpi = ':MMEM:CDIR?'
        return self._vna.query(scpi).strip().strip("'")

    def files(self):
        (size, free_space, files, directories) = self._dir()
        return files

    def directories(self):
        (size, free_space, files, directories) = self._dir()
        return directories

    def file_size(self, path):
        path = pathlib.PureWindowsPath(path)
        location = str(path.parent).replace("/", "\\")
        name = path.name
        original_dir = self.directory()
        if location != ".":
            self.cd(location)
        files = self.files()
        for f in files:
            if f[0].upper() == name.upper():
                if location != ".":
                    self.cd(original_dir)
                return f[1]
        # Else
        if location != ".":
            self.cd(original_dir)
        raise OSError(2, "Could not find file '{0}'".format(path))


    def upload_file(self, local_filename, remote_filename):
        scpi = ":MMEM:DATA '{0}', "
        scpi = scpi.format(remote_filename)
        self._vna.write_raw_no_end(scpi)
        self._vna.write_block_data_from_file(local_filename, 5120)

    def download_file(self, remote_filename, local_filename):
        scpi = ":MMEM:DATA? '{0}'"
        scpi = scpi.format(remote_filename)
        self._vna.write(scpi)
        self_vna.read_block_data_to_file(filename, 5120)

    def _dir(self):
        results = self._vna.query(":MMEM:CAT?").strip();
        results = results.split(',')
        if len(results) < 2:
            raise OSError(0, "Invalid directory information returned from 'MMEM:CAT?'")
        total_file_size = int(results.pop(0).strip())
        free_space = int(results.pop(0).strip())

        directories = []
        files = []
        for i in range(0, len(results)-2, 3):
            if results[i+1].upper().find("<DIR>") != -1:
                directories.append(results[i].strip())
            elif len(results[i+1].strip()) == 0:
                name = results[i].strip()
                size = int(results[i+2].strip())
                files.append((name, size))
            else:
                # Error
                if self._vna.log:
                    self._vna.log.write("This MMEM:DIR? call may have failed because one of the files\n")
                    self._vna.log.write("in the directory contains a ',' in the file name. This is a\n")
                    self._vna.log.write("limitation of the SCPI command, which happens to use comma separators.\n\n")
                    raise OSError(0, "Invalid directory information returned from 'MMEM:CAT?'")
        return (total_file_size, free_space, files, directories)
