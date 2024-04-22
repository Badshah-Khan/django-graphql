from django.db import models
from django.contrib.auth.models import User
from usertype.models import UserType

# Create your models here.
class UserRole(models.Model):
    role = models.ForeignKey(UserType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['role']