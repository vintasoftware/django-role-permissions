from django.conf import settings
from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin
from rolepermissions import roles

ROLEPERMISSIONS_REGISTER_ADMIN = getattr(settings, 'ROLEPERMISSIONS_REGISTER_ADMIN', False)
UserModel = auth.get_user_model()


class RolePermissionsUserAdminMixin(object):
    """ Must be mixed in with an UserAdmin class"""
    def save_related(self, request, form, formsets, change):
        super(RolePermissionsUserAdminMixin, self).save_related(request, form, formsets, change)
        # re-load and take a copy of user's newly saved roles
        user = UserModel.objects.get(pk=form.instance.pk)
        groups = list(user.groups.all())
        # reset user's roles to match the list of groups just saved
        roles.clear_roles(user)
        for g in groups :
            try :
                roles.assign_role(user, g.name)
            except roles.RoleDoesNotExist :
                pass


class RolePermissionsUserAdmin(RolePermissionsUserAdminMixin, UserAdmin):
    pass

if ROLEPERMISSIONS_REGISTER_ADMIN:
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, RolePermissionsUserAdmin)
