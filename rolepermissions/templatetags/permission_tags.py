from __future__ import unicode_literals

from django import template

from rolepermissions.checkers import has_role, has_permission, has_object_permission


register = template.Library()


@register.filter(name='has_role')
def has_role_template_tag(user, role):
    role_list = role.split(',')
    return has_role(user, role_list)


@register.filter(name='can')
def can_template_tag(user, role):
    return has_permission(user, role)


if hasattr(register, 'assignment_tag'):
    tag_registter = register.assignment_tag
else:
    tag_registter = register.simple_tag


@tag_registter(name='can', takes_context=True)
def has_permission_template_tag(context, permission, obj, user=None):
    if not user:
        user = context.get('user')

    if user:
        return has_object_permission(permission, user, obj)

    return False
