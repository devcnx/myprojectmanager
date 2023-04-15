from django.contrib import admin
from .forms import WorkOrderForm
from .models import WorkOrder


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
    filter_horizontal = ('work_order_trips',
                         'work_order_notes', 'work_order_resources')
    fieldsets = (
        ('Work Order Information', {
            'fields': ('work_order_number', 'work_order_project', 'work_order_site', 'work_order_status', 'work_order_trips', 'work_order_notes', 'work_order_resources')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_updated_by = request.user
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)


admin.site.register(WorkOrder, WorkOrderAdmin)
