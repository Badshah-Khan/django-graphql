from django.db import models

# Create your models here.
class Organization(models.Model):
  name = models.CharField(max_length=255)
  org_email = models.CharField(max_length=255, blank=True, null=True)
  org_phone = models.CharField(max_length=255, blank=True, null=True)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  class Meta:
    ordering = ['name']