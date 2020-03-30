from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rolepermissions import roles


class Command(BaseCommand):
    ROLEPERMISSIONS_MODULE = getattr(settings, 'ROLEPERMISSIONS_MODULE', 'roles.py')
    help = "Synchronize auth Groups and Permissions with UserRoles defined in %s." % ROLEPERMISSIONS_MODULE
    version = "1.0.0"

    def get_version(self):
        return self.version

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument(
            '--reset_user_permissions',
            action='store_true',
            dest='reset_user_permissions',
            default=False,
            help='Re-assign all User roles -- resets user Permissions to defaults defined by role(s) !! CAUTION !!',
        )
        parser.add_argument(
            '--all_permissions',
            action='store_true',
            dest='all_permissions',
            default=False,
            help='Create all new permissions instead of only permissions with default true',
        )

    def handle(self, *args, **options):
        # Sync auth.Group with current registered roles (leaving existing groups intact!)
        for role in roles.RolesManager.get_roles():
            group, created = role.get_or_create_group()
            if created:
                self.stdout.write("Created Group: %s from Role: %s" % (group.name, role.get_name()))
            # Sync auth.Permission with permissions for this role
            if options.get('all_permissions', False):
                role.get_all_permissions()
            else:
                role.get_default_true_permissions()

        if options.get('reset_user_permissions', False):  # dj1.7 compat
            # Push any permission changes made to roles and remove any unregistered roles from all auth.Users
            self.stdout.write("Resetting permissions for ALL Users to defaults defined by roles.")

            for user in get_user_model().objects.all():
                user_roles = roles.get_user_roles(user=user)
                roles.clear_roles(user=user)
                for role in user_roles:
                    roles.assign_role(user=user, role=role)
