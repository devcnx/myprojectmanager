from django.contrib import admin
from .models import Rate


class RateAdmin(admin.ModelAdmin):
    list_display = ('rate_type', 'rate_amount')
    search_fields = ('rate_type', 'rate_amount')
    list_filter = ('rate_type', 'rate_amount')
    ordering = ('rate_id',)
    fieldsets = (
        ('Rate Information', {
            'fields': ('rate_type', 'rate_amount')
        }),
    )


admin.site.register(Rate, RateAdmin)
