from django import forms 
from .models import TravelHours, TravelExpense


class TravelHoursForm(forms.ModelForm):
    class Meta:
        model = TravelHours
        fields = '__all__'
        readonly_fields = ('week_ending',)

    def __init__(self, *args, **kwargs):
        super(TravelHoursForm, self).__init__(*args, **kwargs)
        self.fields['travel_hours'].widget.attrs.update(
            {
                'step': '0.25',
                'min': '0',
                'max': '24',
            }
        )


class TravelExpenseForm(forms.ModelForm):
    class Meta:
        model = TravelExpense 
        fields = '__all__'
        readonly_fields = ('week_ending',)

    def __init__(self, *args, **kwargs):
        super(TravelExpenseForm, self).__init__(*args, **kwargs)
        self.fields['expense_amount'].widget.attrs.update(
            {
                'step': '0.25',
                'min': '0',
                'max': '24',
            }
        )