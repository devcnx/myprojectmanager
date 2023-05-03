from django.contrib import admin
from django.db.models import Q
from .forms import MaterialForm
from .models import Material, MaterialAlternativeManufacturerNumber, MaterialVendor, MaterialOrderItem, MaterialOrder


class MaterialAdmin(admin.ModelAdmin):
    form = MaterialForm
    list_display = ('description',
                    'manufacturer', 'manufacturer_number')
    search_fields = ('description', 'manufacturer', 'manufacturer_number')


admin.site.register(Material, MaterialAdmin)


class MaterialAlternativeManufacturerNumberAdmin(admin.ModelAdmin):
    model = MaterialAlternativeManufacturerNumber
    list_display = ('get_material', 'alternative_manufacturer_number')

    def get_material(self, obj):
        return obj.material.description
    get_material.short_description = 'Material'


admin.site.register(MaterialAlternativeManufacturerNumber,
                    MaterialAlternativeManufacturerNumberAdmin)


class MaterialVendorAdmin(admin.ModelAdmin):
    model = MaterialVendor
    list_filter = ('vendor', 'vendor_unit_price', 'vendor_product_link')
    list_display = ('vendor', 'get_material', 'get_manufacturer',
                    'get_manufacturer_number', 'vendor_part_number', 'vendor_unit_price', 'vendor_unit_of_measure')

    def get_material(self, obj):
        return obj.material.description
    get_material.short_description = 'Material'

    def get_manufacturer(self, obj):
        return obj.material.manufacturer
    get_manufacturer.short_description = 'MFR'

    def get_manufacturer_number(self, obj):
        return obj.material.manufacturer_number
    get_manufacturer_number.short_description = 'MFR #'


admin.site.register(MaterialVendor, MaterialVendorAdmin)


admin.site.register(MaterialOrderItem)
admin.site.register(MaterialOrder)
