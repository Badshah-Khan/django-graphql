from django.db import models
from employeedetails.models import Employee

# Create your models here.
class EmployeeAddress(models.Model):
  street = models.CharField(max_length=100)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  postal_code = models.CharField(max_length=10)
  country = models.CharField(max_length=50)
  user = models.ForeignKey(Employee, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  class Meta:
    ordering = ['street']