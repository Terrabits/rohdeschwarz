from .helpers import ellipsis
from io       import StringIO
from sys      import stdout


MAX_PRINT_LENGTH = 100


class Log():
    def __init__(self):
        self._file  = None
        self._pause = False

    def __del__(self):
        if self.is_open:
            self.close()

    @property
    def is_open(self):
        return self._file is not None

    # file io
    def open(self, filename):
        self._file = open(filename, 'w')

    def close(self):
        if self.is_stdout:
            # do not close stdout!
            pass
        else:
            self._file.close()
        self._file = None

    # stdout
    @property
    def is_stdout(self):
        return self._file == stdout

    def use_stdout(self):
        self._file = stdout

    def print(self, text):
        if self.should_not_print:
            return
        self._file.write(text)
        self._file.flush()

    def print_read(self, data, status=None):
        text = StringIO()
        pretty_data = ellipsis(data.strip(), MAX_PRINT_LENGTH)
        text.write(f'Read:     {pretty_data}\n')
        text.write(f'Bytes:    {len(data)}\n')
        if status:
            text.write(f'Status:   {status}\n')
        text.write('\n')
        self.print(text.getvalue())

    def print_write(self, data, status=None):
        text = StringIO()
        pretty_data = ellipsis(data.strip(), MAX_PRINT_LENGTH)
        text.write(f'Write:    "{pretty_data}"\n')
        text.write(f'Bytes:    {len(data)}\n')
        if status:
            text.write(f'Status:   {status}\n')
        text.write('\n')
        self.print(text.getvalue())

    # pause logging
    @property
    def is_paused(self):
        return self._pause

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    # helpers
    @property
    def should_not_print(self):
        if not self.is_open:
            return True
        if self.is_paused:
            return True
        # else
        return False
