class Properties:

    def __init__(self, vsa):
        self._vsa = vsa


    @property
    def is_rohde_schwarz(self):
        id    = self._vsa.id_string()
        parts = id.split(',')
        return 'rohde' in parts[0].lower()


    @property
    def device_type(self):
        id    = self._vsa.id_string()
        parts = id.split(',')
        return parts[1]


    @property
    def part_number(self):
        id    = self._vsa.id_string()
        parts = id.split(',')
        part_no_serial_no = parts[2].split('/')
        return part_no_serial_no[0]


    @property
    def serial_number(self):
        id    = self._vsa.id_string()
        parts = id.split(',')
        part_no_serial_no = parts[2].split('/')
        return part_no_serial_no[1]


    @property
    def firmware_version(self):
        id    = self._vsa.id_string()
        parts = id.split(',')
        return parts[-1]
