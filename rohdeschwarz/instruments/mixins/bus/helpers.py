def to_ellipsis_str(data, max_length):
    dots_len  = 3  # ...
    bytes_len = 3  # b''
    data_max  = max_length - bytes_len - dots_len
    if len(data) <= data_max:
        # no ellipsis
        return str(data)

    # truncate; add ellipsis
    return f'{data[:data_max]}...'
