from django import forms 
from .models import Project 


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project 
        fields = '__all__'
        widgets = {
            'project_start': forms.DateInput(attrs={'type': 'date'}),
            'project_end': forms.DateInput(attrs={'type': 'date'}),
        }
        
        