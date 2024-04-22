from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

# Create your models here.
class UserOrganization(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)