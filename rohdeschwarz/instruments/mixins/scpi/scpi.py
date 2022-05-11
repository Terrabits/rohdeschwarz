from .helpers import raise_if_not_instrument


class ScpiMixin:
    def __init__(self, parent):
        self.parent = parent

    # helpers

    def get_formatted_scpi(self, scpi_str, add_locals={}):
        inputs = locals()
        inputs.update(add_locals)
        return scpi_str.format_map(inputs)

    def raise_if_parent_not_instrument(self):
        return raise_if_not_instrument(self.parent)
