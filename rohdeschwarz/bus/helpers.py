import warnings


def ignore_warnings(function):
    def function_ignore_warnings(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return function(*args, **kwargs)
    return function_ignore_warnings
