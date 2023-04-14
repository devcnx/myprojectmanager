from django import forms 
from .models import Trip 


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ('created_on', 'created_by', 'updated_on', 'updated_by')
        widgets = {
            'trip_start_date': forms.DateInput(attrs={'type': 'date'}),
            'trip_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'trip_end_date': forms.DateInput(attrs={'type': 'date'}),
            'trip_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

        