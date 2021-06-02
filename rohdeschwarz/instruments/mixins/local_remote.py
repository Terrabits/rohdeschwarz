class LocalRemoteMixin:
    def local(self):
        self.write("@LOC")

    def remote(self):
        self.write("@REM")
