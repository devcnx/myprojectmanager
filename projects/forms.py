from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('project_notes', 'is_new_project')
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_number': forms.TextInput(attrs={'class': 'form-control'}),
            'project_start': forms.DateInput(attrs={'type': 'date'}),
            'project_end': forms.DateInput(attrs={'type': 'date'}),
            'project_status': forms.Select(attrs={'class': 'form-control'}),
            'project_contacts': forms.CheckboxSelectMultiple(attrs={'class': 'multiple_select'}),
            'project_sites': forms.CheckboxSelectMultiple(attrs={'class': 'multiple_select'}),
            'created_by': forms.HiddenInput(),
            'last_updated_by': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields['created_by'].initial = self.request.user
            self.fields['created_by'].label = ''
            self.fields['last_updated_by'].initial = self.request.user
            self.fields['last_updated_by'].label = ''
            self.fields['project_status'].initial = 'Bidding'
            self.fields['project_start'].initial = timezone.now().date()
            self.fields['project_end'].initial = timezone.now().date()

    def save(self, commit=True):
        project = super().save(commit=False)
        project.created_by = self.request.user
        project.last_updated_by = self.request.user
        if commit:
            project.save()
        return project

    def save_m2m(self):
        project = super().save(commit=False)
        project.project_contacts.set(self.cleaned_data['project_contacts'])
        project.project_sites.set(self.cleaned_data['project_sites'])
        if commit:
            project.save()
        return project
