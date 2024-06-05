from django.db import models
from organization.models import Organization
from django.contrib.auth.models import User

# Create your models here.
class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=200)
    device_type = models.CharField(max_length=20, null=True)
    device_id = models.CharField(max_length=200, null=True)
    app_version = models.CharField(max_length=10, null=True)
    os_version = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    last_notification_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
