from enum import Enum
from rohdeschwarz.general import unique_alphanumeric_string


class VnaDiagram(object):
    def __init__(self, vna, index=1):
        self._vna = vna
        self._index = index

    def select(self):
        # No select command...
        is_max = self.is_maximized()
        if is_max:
            self.normal_size()
            self.maximize()
        else:
            self.maximize()
            self.normal_size()

    def _title(self):
        scpi = ':DISP:WIND{0}:TITL:DATA?'
        scpi = scpi.format(self._index)
        return self._vna.query(scpi).strip().strip("'")
    def _set_title(self, title):
        scpi = ":DISP:WIND{0}:TITL:DATA '{1}'"
        scpi = scpi.format(self._index, title)
        self._vna.write(scpi)
    title = property(_title, _set_title)

    def _traces(self):
        scpi = ':DISP:WIND{0}:TRAC:CAT?'
        scpi = scpi.format(self._index)
        result = self._vna.query(scpi).strip().strip("'")
        result = result.split(',')
        return result[1::2]
    def _set_traces(self, traces):
        _traces = self._traces()
        scpi = ":DISP:WIND{0}:TRAC:EFE '{1}'"
        for t in traces:
            if not t in _traces:
                self._vna.write(scpi.format(self._index, t))
        for t in _traces:
            if not t in traces:
                self._vna.delete_trace(t)
    traces = property(_traces, _set_traces)

    def autoscale(self):
        raise NotImplementedError(0, 'No SCPI command for autoscaling')

    def is_maximized(self):
        scpi = ":DISP:WIND{0}:MAX?"
        scpi = scpi.format(self._index)
        self._vna.query(scpi).strip() == "1"
    def maximize(self):
        scpi = ":DISP:WIND{0}:MAX 1"
        scpi = scpi.format(self._index)
        self._vna.write(scpi)
    def normal_size(self):
        scpi = ":DISP:WIND{0}:MAX 0"
        scpi = scpi.format(self._index)
        self._vna.write(scpi)

    def save_screenshot(self, filename, image_format='JPG'):
        self.select()
        extension = ".{0}".format(image_format).lower()
        if not filename.lower().endswith(extension):
            filename += extension
        scpi = ":MMEM:NAME '{0}'"
        scpi = scpi.format(filename)
        self._vna.write(scpi)
        scpi = ":HCOP:DEV:LANG {0}"
        scpi = scpi.format(image_format)
        self._vna.write(scpi)
        self._vna.write(":HCOP:PAGE:WIND ACT")
        self._vna.write(":HCOP:DEST 'MMEM'")
        self._vna.write(":HCOP")
        self._vna.pause(5000)
        return self._vna.file.is_file(filename)

    def save_screenshot_locally(self, filename, image_format='JPG'):
        extension = ".{0}".format(image_format).lower()
        unique_filename = unique_alphanumeric_string() + extension
        if not filename.lower().endswith(extension):
            filename += extension
        if self.save_screenshot(unique_filename, image_format):
            self._vna.file.download_file(unique_filename, filename)
            self._vna.file.delete(unique_filename)
            return True
        else:
            return False
