from django import forms
from .models import LaborHours 


class LaborHoursForm(forms.ModelForm):
    class Meta:
        model = LaborHours 
        fields = '__all__'
        readonly_fields = ('week_ending')

    def __init__(self, *args, **kwargs):
        super(LaborHoursForm, self).__init__(*args, **kwargs)
        self.fields['labor_hours'].widget.attrs.update(
            {
                'step': '0.25',
                'min': '0',
                'max': '24',
            }
        )