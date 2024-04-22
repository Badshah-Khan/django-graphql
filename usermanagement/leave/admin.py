from django.contrib import admin
from .models import Leave

# Register your models here.
class LeaveAdmin(admin.ModelAdmin):
  list_display = ("leave_type", "reason",  "from_date", "to_date", "is_approved", "get_name_approvedBy", "get_user_id", "get_organization_id", "created_at", "updated_at")
  
  def get_organization_id(self, obj):
    return obj.organization.id
  
  def get_user_id(self, obj):
    return obj.user.id

  def get_name_approvedBy(self, obj):
    return obj.user.username
  
  get_organization_id.short_description = 'Organization ID'
  get_user_id.short_description = "User ID"
  get_name_approvedBy.short_description = "Approved By"

admin.site.register(Leave, LeaveAdmin)
