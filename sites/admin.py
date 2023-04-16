from django.contrib import admin
from .forms import SiteForm
from .models import SiteType, Site


admin.site.register(SiteType)


class SiteAdmin(admin.ModelAdmin):
    form = SiteForm
    list_display = ('site_id', 'site_name', 'site_type',
                    'address', 'city', 'state', 'zip_code')
    list_filter = ('site_type', 'state')
    search_fields = ('site_name', 'address', 'city', 'state', 'zip_code')


admin.site.register(Site, SiteAdmin)
