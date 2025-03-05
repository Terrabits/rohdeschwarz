def to_state_str(_bool):
    """converts bool to scpi state"""
    return '1' if _bool else '0'


def to_bool(state_str):
    """converts state string to bool"""
    return state_str == "1"
