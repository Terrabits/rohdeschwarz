from .state import to_bool, to_state_str


def to_type(value_str, type):
    """converts scpi value_str to python type"""
    if type is bool:
        # state string
        return to_bool(value_str)
    if type is str:
        # quoted string
        value_str = value_str.strip('"')
        value_str = value_str.strip("'")
        return value_str
    if type is not None:
        return type(value_str)
    # else: type is None
    return value_str


def to_scpi(value, type):
    """converts python type to scpi string"""
    if type is bool:
        return to_state_str(value)
    if type is str:
        # scpi requires quotes
        return f"'{value}'"
    else:
        return str(value)
