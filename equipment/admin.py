from django.contrib import admin
from .models import Equipment 


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_id', 'description')
    search_fields = ('description',)
    list_filter = ('description',)
    ordering = ('equipment_id',)
    list_per_page = 25


admin.site.register(Equipment, EquipmentAdmin)