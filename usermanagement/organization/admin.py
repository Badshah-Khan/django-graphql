from django.contrib import admin
from .models import Organization

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
  list_display = ("name", "org_email",  "org_phone", "created_at", "updated_at")

admin.site.register(Organization, OrganizationAdmin)