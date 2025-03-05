def raise_if_not_instrument(parent):
    raise_if_no_write_method(parent)
    raise_if_no_query_method(parent)


def raise_if_no_write_method(parent):
    if not hasattr(parent, 'write'):
        message = f'parent `{parent}` has no write method'
        raise TypeError(message)


def raise_if_no_query_method(parent):
    if not hasattr(parent, 'query'):
        message = f'parent `{parent}` has no query method'
        raise TypeError(message)
