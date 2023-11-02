class Settings(object):

    def __init__(self, vna):
        # init
        super(Settings, self).__init__()
        self.vna = vna

        # default settings
        self.display         = True
        self.output_power_on = True
