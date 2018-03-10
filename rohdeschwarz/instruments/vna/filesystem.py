from   enum import Enum
import pathlib
import os


class Directory(Enum):
    default = 'DEF'
    embed = '.\\Embedding'
    deembed = '.\\Deembedding'
    cal_groups = '.\\Calibration\\Data'
    cal_kits = '.\\Calibration\\Kits'
    external_tools = '.\\External Tools'
    recall_sets = '.\\RecallSets'
    traces = '.\\Traces'

    def __str__(self):
        return self.value


class FileSystem(object):
    def __init__(self, vna):
        self.__vna = vna

    def cd(self, path):
        if isinstance(path, Directory):
            if path == Directory.default:
                self.__vna.write(":MMEM:CDIR DEF")
            else:
                self.cd(Directory.default)
                scpi = ":MMEM:CDIR '{0}'"
                self.__vna.write(scpi.format(path))
        else:
            scpi = ":MMEM:CDIR '{0}'"
            self.__vna.write(scpi.format(path))

    def is_file(self, path):
        path = pathlib.PureWindowsPath(path)
        location = str(path.parent).replace("/", "\\")
        name = path.name
        original_dir = self.directory()
        if location != ".":
            self.cd(location)
        files = self.files()
        for f in files:
            if f.upper() == name.upper():
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
        return self.__vna.query(scpi).strip().strip("'")

    def files(self):
        return [i[0] for i in self.__files_and_sizes()]

    def directories(self):
        (size, free_space, files, directories) = self.__dir()
        return directories

    def file_size(self, path):
        path = pathlib.PureWindowsPath(path)
        location = str(path.parent).replace("/", "\\")
        name = path.name
        original_dir = self.directory()
        if location != ".":
            self.cd(location)
        files = self.__files_and_sizes()
        for f in files:
            if f[0].upper() == name.upper():
                if location != ".":
                    self.cd(original_dir)
                return f[1]
        # Else
        if location != ".":
            self.cd(original_dir)
        raise OSError(2, "Could not find file '{0}'".format(path))

    def mkdir(self, path):
        scpi = ":MMEM:MDIR '{0}'"
        scpi = scpi.format(path)
        self.__vna.write(scpi)
        self.__vna.pause()

    def move(self, source_path, destination_path):
        scpi = ":MMEM:MOVE '{0}','{1}'"
        scpi = scpi.format(source_path, destination_path)
        self.__vna.write(scpi)
        self.__vna.pause()

    def copy(self, source_path, destination_path):
        scpi = ":MMEM:COPY '{0}','{1}'"
        scpi = scpi.format(source_path, destination_path)
        self.__vna.write(scpi)
        self.__vna.pause()

    def delete(self, filename):
        scpi = ":MMEM:DEL '{0}',FORC"
        scpi = scpi.format(filename)
        self.__vna.write(scpi)
        self.__vna.pause()

    def delete_all(self, path):
        current_dir = self.directory()
        if self.is_directory(path):
            self.cd(path)
            files = self.files()
            for file in files:
                self.delete(file)
            self.cd(current_dir)
            self.__vna.pause()

    def rmdir(self, path):
        scpi = ":MMEM:RDIR '{0}'"
        scpi = scpi.format(path)
        self.__vna.write(scpi)
        self.__vna.pause()

    def upload_file(self, local_filename, remote_filename=None):
        assert os.path.isfile(local_filename)
        assert os.access(local_filename, os.R_OK)
        if not remote_filename:
            remote_filename = pathlib.Path(local_filename).name
        scpi = ":MMEM:DATA '{0}',"
        scpi = scpi.format(remote_filename)
        self.__vna.write_raw_no_end(scpi.encode())
        self.__vna.write_block_data_from_file(local_filename, os.path.getsize(local_filename) + 20)

    def download_file(self, remote_filename, local_filename):
        size_B = self.file_size(remote_filename)

        scpi = ":MMEM:DATA? '{0}'"
        scpi = scpi.format(remote_filename)
        self.__vna.write(scpi)
        self.__vna.read_block_data_to_file(local_filename, size_B + 20)

    def __dir(self):
        results = self.__vna.query(":MMEM:CAT?").strip();
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
                if self.__vna.log:
                    self.__vna.log.write("This MMEM:DIR? call may have failed because one of the files\n")
                    self.__vna.log.write("in the directory contains a ',' in the file name. This is a\n")
                    self.__vna.log.write("limitation of the SCPI command, which happens to use comma separators.\n\n")
                    raise OSError(0, "Invalid directory information returned from 'MMEM:CAT?'")
        return (total_file_size, free_space, files, directories)

    def __files_and_sizes(self):
        (size, free_space, files, directories) = self.__dir()
        return files
