from django.db import models
from organization.models import Organization
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=20, null=True)
    message = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, default='Pending')
    priority = models.CharField(max_length=10, null=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True)
    error_message = models.CharField(null=True)
    url = models.CharField(null=True)
    expiration_date = models.DateTimeField()
    action_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
