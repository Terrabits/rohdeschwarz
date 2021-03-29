# for IEEE 488.2 Definite Length Arbitrary Block Response Data
# aka "block data"


def to_block_data(data_bytes):
    length_str = str(len(data_bytes))
    header     = f'#{len(length_str)}{length_str}'
    return header.encode() + data_bytes


def from_block_data(block_data):
    # get length string from header
    str_length  = int(block_data[1])
    str_end     = 2 + str_length
    length_str  = block_data[2:str_end]

    data_length = int(length_str)

    # get data from block
    data_end = str_end + data_length
    return block_data[str_end:data_end]
