from django import forms
from .models import Site


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        exclude = ('added_by', 'modified_by')
        labels = {
            'site_id': 'Site #',
            'zip_code': 'Zip',
        }
