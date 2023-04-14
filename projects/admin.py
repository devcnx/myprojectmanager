from django.contrib import admin
from .forms import ProjectForm 
from .models import Project 


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm 
    list_display = ('project_id', 'project_name', 'project_number', 'project_status', 'project_start', 'project_end', 
                    'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    search_fields = ('project_name', 'project_number', 'project_status', 'project_contacts', 'project_start', 'project_end', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    list_filter = ('project_status', 'project_contacts', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    ordering = ('project_start', 'project_end')
    filter_horizontal = ('project_contacts', 'project_sites')
    fieldsets = (
        ('Project Information', {
            'fields': ('project_name', 'project_number', 'project_status', 'project_start', 'project_end', 'project_contacts', 'project_sites')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user 
        obj.last_updated_by = request.user 
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)


admin.site.register(Project, ProjectAdmin)