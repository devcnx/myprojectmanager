from django.contrib import admin
from .forms import BidForm
from .models import Bid 


class BidAdmin(admin.ModelAdmin):
    form = BidForm 
    list_display = ('bid_id', 'bid_type', 'bid_status', 'bid_project', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    search_fields = ('bid_type', 'bid_status', 'bid_project', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    list_filter = ('bid_type', 'bid_status', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    ordering = ('-created_on',)
    fieldsets = (
        ('Bid Information', {
            'fields': ('bid_type', 'bid_status', 'bid_project')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user 
        obj.last_updated_by = request.user 
        super().save_model(request, obj, form, change)

admin.site.register(Bid, BidAdmin)