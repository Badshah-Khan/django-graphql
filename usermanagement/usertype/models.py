from django.db import models
from organization.models import Organization

# Create your models here.
class UserType(models.Model):
    role = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        ordering = ['role']