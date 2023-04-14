from django import forms 
from .models import Project 


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project 
        exclude = ('created_on', 'created_by', 'last_updated_on', 'last_updated_by', 'is_new_project')
        widgets = {
            'project_start': forms.DateInput(attrs={'type': 'date'}),
            'project_end': forms.DateInput(attrs={'type': 'date'}),
        }
        