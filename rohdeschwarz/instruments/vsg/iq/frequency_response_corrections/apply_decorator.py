def apply(method):

    def applied_method(self, *args, **kwargs):
        method(self, *args, **kwargs)
        self.source.iq.frequency_response_corrections.user_data.apply()

    return applied_method
