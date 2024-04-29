from django.db import models
from organization.models import Organization

# Create your models here.
class Address(models.Model):
  street = models.CharField(max_length=100)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  postal_code = models.CharField(max_length=10)
  country = models.CharField(max_length=50)
  lat = models.CharField(max_length=20, blank=True, null=True)
  long = models.CharField(max_length=20, blank=True, null=True)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  class Meta:
    ordering = ['street']