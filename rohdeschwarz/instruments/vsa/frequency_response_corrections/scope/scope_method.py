def scope_method(method):

    def scoped_method(self, *args, **kwargs):
        self.set_scope()
        method(self, *args, **kwargs)

    return scoped_method
