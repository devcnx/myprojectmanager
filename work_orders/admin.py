from django.contrib import admin
from .forms import WorkOrderForm, WorkOrderTripForm
from .models import WorkOrder, WorkOrderTrip


class WorkOrderAdmin(admin.ModelAdmin):
    form = WorkOrderForm
    list_display = ('work_order_id', 'work_order_number', 'work_order_project', 'work_order_site',
                    'work_order_status', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    search_fields = ('work_order_number', 'work_order_project', 'work_order_site',
                     'work_order_status', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    list_filter = ('work_order_project', 'work_order_site', 'work_order_status',
                   'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    readonly_fields = ('work_order_number',
                       'work_order_project', 'work_order_site')
    ordering = ('work_order_number',)
    filter_horizontal = ('work_order_notes', 'work_order_resources')
    fieldsets = (
        ('Work Order Information', {
            'fields': ('work_order_number', 'work_order_project', 'work_order_site', 'work_order_status', 'work_order_notes', 'work_order_resources')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_updated_by = request.user
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)

    def get_trip_count_for_work_order(self, obj):
        work_order_trip = WorkOrderTrip.objects.filter(work_order=obj)
        return work_order_trip.count()


admin.site.register(WorkOrder, WorkOrderAdmin)


class WorkOrderTripAdmin(admin.ModelAdmin):
    form = WorkOrderTripForm
    ordering = ('trip_id',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_updated_by = request.user
        obj.work_order = WorkOrder.objects.get(pk=obj.work_order_id)
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)


admin.site.register(WorkOrderTrip, WorkOrderTripAdmin)
