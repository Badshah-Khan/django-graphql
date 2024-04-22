from django.contrib import admin
from .models import UserPermission

# Register your models here.
class UserPermissionAdmin(admin.ModelAdmin):
  list_display = ("get_permission_id", "get_user_id", "get_organization_id")

  def get_organization_id(self, obj):
    return obj.organization.id
  
  def get_permission_id(self, obj):
    return obj.permission.id
  
  def get_user_id(self, obj):
    return obj.user.id
  
  get_organization_id.short_description = 'Organization ID'
  get_user_id.short_description = "User ID"
  get_permission_id.short_description = "Permission ID"

admin.site.register(UserPermission, UserPermissionAdmin)