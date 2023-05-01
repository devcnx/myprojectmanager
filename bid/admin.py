from django.contrib import admin
from .forms import AdminBidForm
from .models import Bid, BidMaterial, BidEquipment


class BidAdmin(admin.ModelAdmin):
    form = AdminBidForm
    list_display = ('bid_id', 'bid_type', 'bid_status', 'bid_due_date', 'bid_due_time', 'bid_project',
                    'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    search_fields = ('bid_type', 'bid_status', 'bid_project',
                     'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    list_filter = ('bid_type', 'bid_status', 'created_on',
                   'created_by', 'last_updated_on', 'last_updated_by')
    ordering = ('-created_on',)
    filter_horizontal = ('bid_labor_hours', 'bid_travel_hours',
                         'bid_travel_expenses', 'bid_equipment')
    readonly_fields = ('created_on', 'created_by',
                       'last_updated_on', 'last_updated_by')
    fieldsets = (
        ('Bid Information', {
            'fields': ('bid_type', 'bid_status', 'bid_project', 'bid_due_date', 'bid_due_time')
        }),
        ('Bid Labor', {
            'fields': ('bid_labor_hours',)
        }),
        ('Bid Travel', {
            'fields': ('bid_travel_hours', 'bid_travel_expenses')
        }),
        ('Bid Materials', {
            'fields': ('bid_materials',)
        }),
        ('Bid Equipment', {
            'fields': ('bid_equipment',)
        }),
        (None, {
            'fields': ('bid_submitted', 'bid_submitted_by')
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_updated_by = request.user
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)


admin.site.register(Bid, BidAdmin)


class BidMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'quantity')
    search_fields = ('material', 'quantity')
    list_filter = ('material', 'quantity')
    ordering = ('id',)
    readonly_fields = ('id',)
    fieldsets = (
        ('Bid Material Information', {
            'fields': ('material', 'quantity', 'unit_of_measure', 'unit_price')
        }),
    )


admin.site.register(BidMaterial, BidMaterialAdmin)


class BidEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'quantity')
    search_fields = ('equipment', 'quantity')
    list_filter = ('equipment', 'quantity')
    ordering = ('id',)
    readonly_fields = ('id',)
    fieldsets = (
        ('Bid Equipment Information', {
            'fields': ('equipment', 'quantity', 'unit_price')
        }),
    )


admin.site.register(BidEquipment, BidEquipmentAdmin)
