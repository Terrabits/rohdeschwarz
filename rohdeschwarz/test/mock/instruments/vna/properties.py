class Properties(object):
    def __init__(self, vna, model, ports):
        super(Properties, self).__init__()
        self.vna = vna
        self.model             = model
        self.physical_ports    = ports
        # self.catalog_no        = '1311.60.1072'
        # self.serial_number     = '100104'
        self.serial_number     = '1311601072100104'
        self.firmware_version  = '2.84.0.130'
        self.options_list      = []

        self.minimum_frequency_Hz = 0
        self.maximum_frequency_Hz = float('inf')
