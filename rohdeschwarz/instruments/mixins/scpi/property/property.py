from .get import create_get_function
from .set import create_set_function


def scpi_property(scpi_tree, type=None, read_only=False):
    get = create_get_function(scpi_tree, type)
    set = None if read_only else create_set_function(scpi_tree, type)
    return property(get, set)
