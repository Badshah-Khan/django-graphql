from django.contrib import admin
from .models import Permission

# Register your models here.
class PermissionAdmin(admin.ModelAdmin):
  list_display = ("permission_name", "description")

admin.site.register(Permission, PermissionAdmin)