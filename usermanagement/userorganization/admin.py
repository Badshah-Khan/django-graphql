from django.contrib import admin
from .models import UserOrganization

# Register your models here.
class UserOrganizationAdmin(admin.ModelAdmin):
  list_display = ("user", "get_organization_id")

  def get_organization_id(self, obj):
    return obj.organization.name

  get_organization_id.short_description = 'Organization Name'

admin.site.register(UserOrganization, UserOrganizationAdmin)