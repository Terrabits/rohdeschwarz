from ..types import to_type


def create_get_function(scpi_tree, type):
    def get_function(self):
        nonlocal scpi_tree, type
        self.raise_if_parent_not_instrument()
        tree    = self.get_formatted_scpi(scpi_tree)
        command = f'{tree}?'
        value   = self.parent.query(command)
        return to_type(value, type)
    return get_function
