import datetime
import calendar

class Log:

	def __init__(self, filename, appName, version):
		self._file = None
		self.reset(filename, appName, version)

	def reset(self, filename, appName, version):
		self._file = None
		self._filename = filename
		self._appName = appName
		self._version = version
		return self.open()

	def open(self):
		if self.closed():
			self._file = open(self._filename, 'w')
		return not self.closed()

	def close(self):
		self._file.close()
		self._file = None

	def opened(self):
		return not self.closed()

	def closed(self):
		if not self._file:
			return True
		else:
			return self._file.closed

	def printHeader(self):
		#R&S <_appName> Version <_version>
		#(C) 2015 Rohde & Schwarz America
		#
		#Mon Jul 6 15:05:51 2015
		#
		if self.closed():
			return False
		today = datetime.datetime.now()
		self.printLine("{0} Version {1}".format(self._appName, self._version))
		self.printLine("(C) {0} Rohde & Schwarz\n".format(today.year))
		self.printLine(today.strftime('%a %d %b %H:%M:%S %Y\n'))
		return True

	def print(self, text):
		if self.closed():
			return False
		self._file.write(text)
		return True

	def printLine(self, text):
		if self.closed():
			return False
		self._file.write(text)
		self._file.write('\n')
		return True


# End Log
