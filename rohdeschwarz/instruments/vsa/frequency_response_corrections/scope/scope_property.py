def scope_property(prop):

    current_getter = prop.fget
    current_setter = prop.fset

    def getter(self):
        self.set_scope()
        return current_getter(self)

    prop = prop.getter(getter)

    if current_setter is None:
        return prop

    def setter(self, value):
        self.set_scope()
        current_setter(self, value)

    return prop.setter(setter)
