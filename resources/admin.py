from django.contrib import admin
from .models import ResourceStatus, ResourceCompany, Resource


admin.site.register(ResourceStatus)
admin.site.register(ResourceCompany)
admin.site.register(Resource)
