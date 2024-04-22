from django.contrib import admin
from .models import Attendance

# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
  list_display = ("date", "in_time",  "out_time", "get_user_id", "get_organization_id", "created_at", "updated_at")
  def get_organization_id(self, obj):
    return obj.organization.id
  
  def get_user_id(self, obj):
    return obj.user.id

  get_organization_id.short_description = 'Organization ID'
  get_user_id.short_description = "User ID"

admin.site.register(Attendance, AttendanceAdmin)
