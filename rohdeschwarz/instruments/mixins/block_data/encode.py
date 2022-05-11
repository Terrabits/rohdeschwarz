def encode(data):
    """encode `data` bytes as IEEE 488.2 Block Data"""
    assert isinstance(data, bytes)
    return create_header_for(data) + data


# helpers

def create_header_for(data):
    size_str = str(len(data))
    header   = f'#{len(size_str)}{size_str}'
    return header.encode()
