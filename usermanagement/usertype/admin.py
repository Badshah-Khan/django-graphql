from django.contrib import admin
from .models import UserType

# Register your models here.
class UserTypeAdmin(admin.ModelAdmin):
  list_display = ("role", "get_organization_id")

  def get_organization_id(self, obj):
    return obj.organization.id
  
  get_organization_id.short_description = 'Organization ID'

admin.site.register(UserType, UserTypeAdmin)