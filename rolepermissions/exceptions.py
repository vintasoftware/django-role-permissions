from __future__ import unicode_literals


class CheckerNotRegistered(Exception):
    pass


class RoleDoesNotExist(Exception):
    pass


class RolePermissionScopeException(Exception):
    pass
