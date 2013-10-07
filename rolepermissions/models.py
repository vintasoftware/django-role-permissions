
from django.db import models
from django.contrib.auth import get_user_model


class UserRole(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='role')
    role_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user.get_full_name() + ' - ' + self.role_name


class UserPermission(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='+')
    permission_name = models.CharField(max_length=255)
    is_granted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.get_full_name() + ' - ' + self.permission_name + ' - ' + str(self.is_granted)
