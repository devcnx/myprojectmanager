from django.contrib import admin
from .models import Equipment 


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('description',)
    list_display_links = ('description',)
    search_fields = ('description',)
    ordering = ('equipment_id',)
    list_per_page = 25


admin.site.register(Equipment, EquipmentAdmin)