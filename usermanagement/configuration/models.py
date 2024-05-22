from django.db import models
from organization.models import Organization

# Create your models here.
class Configuration(models.Model):
    organization_name = models.CharField(max_length=50)
    configuration = models.JSONField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
