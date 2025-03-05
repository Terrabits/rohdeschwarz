from ..types import to_scpi


def create_set_function(scpi_tree, type):
    def set_function(self, value):
        nonlocal scpi_tree, type
        self.raise_if_parent_not_instrument()
        tree    = self.get_formatted_scpi(scpi_tree)
        value   = to_scpi(value, type)
        command = f'{tree} {value}'
        self.parent.write(command)
    return set_function
