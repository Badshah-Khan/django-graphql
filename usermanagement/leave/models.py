from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

# Create your models here.
class Leave(models.Model):
  leave_type = models.CharField(max_length=20)
  reason = models.CharField(max_length=255, blank=True, null=True)
  from_date = models.DateField()
  to_date = models.DateField()
  is_approved = models.BooleanField(default=False)
  approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='approved_leaves')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_leaves')
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  class Meta:
    ordering = ['-id']