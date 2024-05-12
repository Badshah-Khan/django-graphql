from django.db import models
from organization.models import Organization

# Create your models here.
class Holydays(models.Model):
    ocation = models.CharField()
    description = models.TextField()
    num_of_days = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)