from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization
from permission.models import Permission

# Create your models here.
class UserPermission(models.Model):
  permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)