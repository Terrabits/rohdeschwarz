from ..types import to_scpi


def get_inputs(input_types, *args, **kwargs):
    # use list;
    # take out args (pop) until empty
    args = list(args)

    # get input values
    inputs = {}
    for input, type in input_types.items():
        # value for `input`?
        if args:
            # take from args
            value = args.pop(0)
        elif input in kwargs:
            # take from kwargs
            value = kwargs[input]
        else:
            # missing method argument
            message = f'missing method argument `{input}`'
            raise TypeError(message)

        # add value to inputs
        inputs[input] = to_scpi(value, type)
    return inputs
