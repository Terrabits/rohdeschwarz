

class MockBus(object):
	def __init__(self, reads=[]):
		self.reset(reads)

	def __del__(self):
		return

	def open(self, *args):
		return

	def close(self):
		return

	def read(self):
		if self.reads:
			return self.reads.pop(0)
		else:
			raise EOFError("MockBus object has no more reads")

	def write(self, scpi):
		self.writes.append(scpi)

	def read_raw_no_end(self, buffer_size=1024):
		return self.read()

	def write_raw_no_end(self, buffer):
		self.write(buffer)

	def status_string(self):
		status = 'Mockbus has {0} writes, {1} reads left'
		status = status.format(len(self.writes), len(self.reads))
		return status

	def reset(self, reads=[]):
		self.reads       = reads
		self.writes      = []
		self.buffer_size = 1024
		self.delimiter   = '\n'
		self.timeout_ms  = 1000
