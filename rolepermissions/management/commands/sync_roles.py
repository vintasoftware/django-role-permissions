from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rolepermissions import roles

UserModel = get_user_model()

class Command(BaseCommand):
    ROLEPERMISSIONS_MODULE = getattr(settings, 'ROLEPERMISSIONS_MODULE', 'roles.py')
    help = "Synchronize auth Groups and Permissions with UserRoles defined in %s."%ROLEPERMISSIONS_MODULE

    def handle(self, *args, **options):
        # Sync auth.Group with current registered roles (leaving existing groups intact!)
        for role in roles.RolesManager.get_roles() :
            group, created = Group.objects.get_or_create(name=role.get_name())
            if created:
                self.stdout.write("Created Group: %s from Role: %s"%(group.name, role.get_name()))
            # Sync auth.Permission with permissions for this role
            role.get_default_true_permissions()

        # Push any permission changes made to roles and remove any unregistered roles from all auth.Users
        for user in UserModel.objects.all():
            user_roles = roles.get_user_roles(user)
            roles.clear_roles(user)
            for role in user_roles:
                roles.assign_role(user, role)
