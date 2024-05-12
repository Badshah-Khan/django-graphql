from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

# Create your models here.
class Message(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_message')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_message')
  date = models.DateTimeField()
  content = models.TextField()
  is_read = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  is_accepted = models.BooleanField(default=False)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  deleted_at = models.DateTimeField(blank=True, null=True)