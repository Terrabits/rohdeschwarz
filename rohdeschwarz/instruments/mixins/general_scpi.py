class GeneralScpiMixin:
    @property
    def id_string(self):
        return self.query('*IDN?').strip()

    @property
    def options_string(self):
        return self.query("*OPT?").strip()

    def preset(self):
        self.write("*RST")
