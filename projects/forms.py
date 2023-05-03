from datetime import datetime
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_number': forms.TextInput(attrs={'class': 'form-control'}),
            'project_contacts': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'project_start': forms.DateInput(attrs={'type': 'date', 'value': datetime.now().strftime('%Y-%m-%d')}),
            'project_end': forms.DateInput(attrs={'type': 'date', 'value': datetime.now().strftime('%Y-%m-%d')}),
            'project_sites': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
