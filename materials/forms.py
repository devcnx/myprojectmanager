from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ('created_on', 'created_by',
                   'last_updated_on', 'last_updated_by')
        widgets = {
            'material_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
