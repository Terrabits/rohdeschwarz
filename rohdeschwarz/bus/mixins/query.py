class QueryMixin(object):
    def query(self, command_str):
        self.write(command_str)
        return self.read().strip()

    def query_raw_no_end(self, command_bytes):
        self.write_raw_no_end(command_bytes)
        return self.read_raw_no_end()
