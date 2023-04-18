from django.contrib import admin
from .forms import MaterialForm
from .models import Material, MaterialVendor


# admin.site.register(Material)

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('description',
                    'manufacturer', 'manufacturer_number')
    form = MaterialForm


admin.site.register(Material, MaterialAdmin)

admin.site.register(MaterialVendor)
