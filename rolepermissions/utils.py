from __future__ import unicode_literals

import re
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable


def user_is_authenticated(user):
    if isinstance(user.is_authenticated, Callable):
        authenticated = user.is_authenticated()
    else:
        authenticated = user.is_authenticated

    return authenticated


def camelToSnake(s):
    """
    https://gist.github.com/jaytaylor/3660565
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    _underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
    _underscorer2 = re.compile('([a-z0-9])([A-Z])')

    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def snake_to_title(s):
    return ' '.join(x.capitalize() for x in s.split('_'))


def camel_or_snake_to_title(s):
    return snake_to_title(camelToSnake(s))
