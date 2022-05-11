def is_complete(block_data):
    assert isinstance(block_data, bytes)
    index, data_size = parse_index_size_from_header(block_data)
    return len(block_data) >= index + data_size


def decode(block_data):
    """Decodes IEEE 488.2 Block Data to original bytes"""
    assert isinstance(block_data, bytes)
    index, data_size = parse_index_size_from_header(block_data)
    if len(block_data) < index + data_size:
        raise ValueError('error: not enough data to reconstruct block')

    # return raw data
    start = index
    stop  = index + data_size
    return block_data[start:stop]


# helpers

def parse_index_size_from_header(block_data):
    if len(block_data) < 2:
        raise ValueError('error: too few data')
    if block_data[0:1] != b'#':
        raise ValueError('error: header not found')
    try:
        string_size = int(block_data[1:2])
    except ValueError as error:
        new_error = ValueError('error: could not parse header size')
        raise new_error from error

    header_size = 2 + string_size
    if len(block_data) < header_size:
        raise ValueError('error: cannot parse header because too few data')

    data_size_str = block_data[2:2 + string_size]
    try:
        data_size = int(data_size_str)
    except ValueError as error:
        new_error = ValueError('error: could not parse header size')
        raise new_error from error
    return header_size, data_size
