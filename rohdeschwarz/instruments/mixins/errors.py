class ErrorsMixin:
    @property
    def errors(self):
        errors     = []
        next_error = self._next_error()
        while next_error is not None:
            errors.append(next_error)
            next_error = self._next_error()
        return errors

    def clear_status(self):
        self.write("*CLS")


    # helpers
    def _next_error(self):
        # format: code,"message"
        next_error  = self.query('SYST:ERR?').strip()

        comma_index = next_error.find(',')
        code        = int(next_error[:comma_index])
        if code == 0:
            # no error
            return None

        # error
        message = result[comma_index+2:-1]
        return code, message
