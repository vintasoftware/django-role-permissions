from django.conf import settings
from django.contrib import admin, auth
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from rolepermissions import roles

ROLEPERMISSIONS_REGISTER_ADMIN = getattr(settings, 'ROLEPERMISSIONS_REGISTER_ADMIN', False)
UserModel = auth.get_user_model()


class RolePermissionsUserAdminMixin(object):
    """ Must be mixed in with an UserAdmin class"""
    def save_related(self, request, form, formsets, change):
        user = UserModel.objects.get(pk=form.instance.pk)
        old_user_roles = set(r.get_name() for r in roles.get_user_roles(user))
        super(RolePermissionsUserAdminMixin, self).save_related(request, form, formsets, change)

        new_user_groups = set(g.name for g in user.groups.all())

        for role_name in (old_user_roles - new_user_groups):  # roles removed from User's groups
            try:  # put the recently removed group back, let rolepermissions remove it...
                group = Group.objects.get(name=role_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
            roles.remove_role(user, role_name)

        for group_name in (new_user_groups - old_user_roles):  # groups potentially added to User's roles
            try:
                roles.assign_role(user, group_name)
            except roles.RoleDoesNotExist:
                pass


class RolePermissionsUserAdmin(RolePermissionsUserAdminMixin, UserAdmin):
    pass


if ROLEPERMISSIONS_REGISTER_ADMIN:
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, RolePermissionsUserAdmin)
