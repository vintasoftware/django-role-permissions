from __future__ import unicode_literals

from rolepermissions.exceptions import CheckerNotRegistered


class PermissionsManager(object):
    _checkers = {}

    @classmethod
    def register_checker(cls, name, function):
        cls._checkers[name] = function

    @classmethod
    def get_checkers(cls):
        return cls._checkers

    @classmethod
    def retrieve_checker(cls, checker_name):
        if checker_name in cls._checkers:
            return cls._checkers[checker_name]

        raise CheckerNotRegistered('Checker with name %s was not registered' % checker_name)


def register_object_checker(name=None):
    def fuction_decorator(func):
        checker_name = name if name else func.__name__
        PermissionsManager.register_checker(checker_name, func)
    return fuction_decorator
