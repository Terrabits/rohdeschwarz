def apply_property(prop):

    current_setter = prop.fset

    if current_setter is None:
        return prop

    def setter(self, value):
        current_setter(self, value)
        self.source.iq.frequency_response_corrections.user_data.apply()

    return prop.setter(setter)
