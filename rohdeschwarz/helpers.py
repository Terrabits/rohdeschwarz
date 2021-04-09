from   math import factorial
import uuid


def number_of_thrus(port_count):
    if port_count <= 0:
        raise ValueError("number_of_thrus() not defined for port count less than 1")
    if port_count == 1:
        return 0
    # else
    return factorial(port_count) / (2 * factorial(port_count - 2))


def unique_alphanumeric_string():
    unique_string = str(uuid.uuid4())
    unique_string = unique_string.replace('-', '')
    return unique_string


def ellipsis(data, max_length):
    if len(data) <= max_length:
        return data

    # truncate and add ellipsis
    dot_dot_dot = '...' if isinstance(data, str) else b'...'
    return data[:max_length] + dot_dot_dot
