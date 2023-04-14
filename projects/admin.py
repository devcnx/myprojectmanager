from django.contrib import admin
from .forms import ProjectForm 
from .models import Project 


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm 
    list_display = ('project_id', 'project_name', 'project_number', 'project_status', 'project_start', 'project_end', 
                    'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    search_fields = ('project_name', 'project_number', 'project_status', 'project_start', 'project_end', 
                        'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    list_filter = ('project_status', 'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
    date_hierarchy = 'project_start'
    ordering = ('project_start', 'project_end')
    filter_horizontal = ('project_sites',)
    fieldsets = (
        ('Project Information', {
            'fields': ('project_name', 'project_number', 'project_status', 'project_start', 'project_end', 'project_sites')
        }),
    )


admin.site.register(Project, ProjectAdmin)