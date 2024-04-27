from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    dob = models.DateField(blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)