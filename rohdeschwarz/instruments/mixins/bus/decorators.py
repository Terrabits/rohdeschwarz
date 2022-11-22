from   .helpers import to_ellipsis_str
import logging


def log_read(read_function):
    # wrap read function
    def read_with_log(self, *args, **kwargs):
        # call read function to read data
        data = read_function(self, *args, **kwargs)

        # log
        data_str = to_ellipsis_str(data, max_length=50)
        message  = f'{self.instr_name}.read:  {data_str}'
        logging.info(message)
        return data
    return read_with_log


def log_write(write_function):
    def write_with_log(self, data):
        data_str = to_ellipsis_str(data, max_length=50)
        message  = f'{self.instr_name}.write: {data_str}'
        logging.info(message)
