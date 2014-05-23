import sys
from six import string_types
from itertools import izip

type_map = {
    "register": string_types,
    "int": int,
    "any": object
}


def accepts(*types):
    '''Function decorator. Checks decorated function's arguments are
    of the expected types.

    Parameters:
    types -- The expected types of the inputs to the decorated function.
             Must specify type for each parameter.
    '''
    try:
        def decorator(f):
            def newf(*args):
                valid = True
                for expected_type, arg in izip(types, args[1:]):
                    if not isinstance(arg, type_map[expected_type]):
                        valid = False
                        msg = "{} not {} in '{}' instruction".format(arg, expected_type, f.__name__)
                        break

                if not valid:
                    raise TypeError, msg

                return f(*args)
            newf.__name__ = f.__name__
            return newf
        return decorator
    except TypeError, msg:
        raise TypeError, msg
