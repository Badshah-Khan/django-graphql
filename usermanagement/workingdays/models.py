from django.db import models

# Create your models here.
class WorkingDays(models.Model):
    total_working_days = models.IntegerField()
    total_days = models.IntegerField(blank=True, null=True)
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    year = models.IntegerField(null=True)
    month = models.CharField(max_length=15)