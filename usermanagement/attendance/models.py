from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

# Create your models here.
class Attendance(models.Model):
  date = models.DateField()
  in_time = models.TimeField(blank=True, null=True)
  out_time = models.TimeField(blank=True, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  class Meta:
    ordering = ['date']