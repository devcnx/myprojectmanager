from django import forms
from .models import LaborHours


class LaborHoursForm(forms.ModelForm):
    class Meta:
        model = LaborHours
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LaborHoursForm, self).__init__(*args, **kwargs)
        self.fields['labor_hours'].widget.attrs.update(
            {
                'step': '0.25',
                'min': '0',
                'max': '24',
            }
        )
        self.fields['labor_hours_quantity'].widget.attrs.update(
            {
                'step': '0.25',
                'min': '0',
                'max': '24',
            }
        )
