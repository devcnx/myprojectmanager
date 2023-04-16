from django.contrib import admin
from .models import VendorType, Vendor, VendorContact


admin.site.register(VendorType)
admin.site.register(Vendor)
admin.site.register(VendorContact)
