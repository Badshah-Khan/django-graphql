from django.contrib import admin
from .models import UserRole

# Register your models here.
class UserRoleAdmin(admin.ModelAdmin):
  list_display = ("get_usertype_id", "get_user_id")

  def get_usertype_id(self, obj):
    return obj.usertype.id
  
  def get_user_id(self, obj):
    return obj.user.id
  
  get_usertype_id.short_description = 'Role ID'
  get_user_id.short_description = "User ID"

admin.site.register(UserRole, UserRoleAdmin)