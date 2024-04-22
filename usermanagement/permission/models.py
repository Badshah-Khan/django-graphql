from django.db import models

# Create your models here.
class Permission(models.Model):
  permission_name = models.CharField(max_length=20)
  description = models.TextField(blank=True, null=True)

  class Meta:
    ordering = ['permission_name']
