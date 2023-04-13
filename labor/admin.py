from django.contrib import admin
from .models import LaborHours


class LaborHoursAdmin(admin.ModelAdmin):
    list_display = ('week_ending', 'labor_date', 'labor_resource', 'labor_type', 'labor_hours', 'labor_created', 'labor_updated')
    list_filter = ('labor_type', 'labor_resource', 'labor_created', 'labor_updated')
    search_fields = ('labor_type', 'labor_resource', 'labor_created', 'labor_updated')
    ordering = ('-week_ending',)
    date_hierarchy = 'week_ending'
    save_on_top = True


admin.site.register(LaborHours, LaborHoursAdmin)