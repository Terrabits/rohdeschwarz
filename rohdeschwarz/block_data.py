# for IEEE 488.2 Definite Length Arbitrary Block Response Data
# aka "block data"


MAX_HEADER_LENGTH = 11  # len(b'#9123456789')


def to_block_data(data_bytes):
    length_str = str(len(data_bytes))
    header     = f'#{len(length_str)}{length_str}'
    return header.encode() + data_bytes


def parse_header(partial_block_data):
    str_length  = int(partial_block_data[1:2])
    str_end     = 2 + str_length
    length_str  = partial_block_data[2:str_end]
    data_length = int(length_str)
    data        = partial_block_data[str_end:]
    return data_length, data


def from_block_data(block_data):
    data_length, data = parse_header(block_data)
    if len(data) < data_length:
        raise EOFError(f'missing block data: received {len(data)} of {data_length} bytes')
    return data[:data_length]




    # get data from block
    data_end = str_end + data_length
    return block_data[str_end:data_end]
