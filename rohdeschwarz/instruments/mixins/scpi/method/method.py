from ..types import to_type
from .inputs import get_inputs


def scpi_method(scpi_command, *, return_type=None, **input_types):
    """creates a method in ScpiMixin class for `scpi_command` with `**input_types` and `return_type`

    Example:

    ```python
    # in ScpiMixin class defininition:
    manual_trigger = scpi_method('*TRG')
    ```
    """
    return new_scpi_method(scpi_command, input_types, return_type)

# helpers

def new_scpi_method(scpi_command, input_types={}, return_type=None):
    def scpi_method(self, *args, **kwargs):
        nonlocal scpi_command, input_types
        self.raise_if_parent_not_instrument()
        inputs  = get_inputs(input_types, *args, **kwargs)
        command = self.get_formatted_scpi(scpi_command, inputs)
        self.parent.write(command)
        if return_type is not None:
            value = self.parent.read()
            value = to_type(value, return_type)
            return value
    return scpi_method
