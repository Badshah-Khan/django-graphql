from django.contrib import admin
from .models import Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
  list_display = ("street", "city",  "state", "postal_code", "country", "get_organization_id")

  def get_organization_id(self, obj):
    return obj.organization.id

  get_organization_id.short_description = 'Organization ID'

admin.site.register(Address, AddressAdmin)