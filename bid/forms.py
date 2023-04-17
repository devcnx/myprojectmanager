from django import forms
from django.forms import formset_factory
from labor.models import LaborHours
from rates.models import Rate
from travel.models import TravelHours, TravelExpense
from .models import Bid


class AdminBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('created_on', 'created_by',
                   'last_updated_on', 'last_updated_by')


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        exclude = ('bid_labor_hours', 'bid_travel_hours',
                   'bid_travel_expenses', 'bid_materials', 'bid_equipment',
                   'created_on', 'created_by', 'last_updated_on', 'last_updated_by')


class BidLaborHoursForm(forms.Form):
    labor_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    labor_type = forms.ChoiceField(
        choices=LaborHours.LABOR_HOURS_CHOICES)
    labor_rate = forms.ModelChoiceField(
        queryset=Rate.objects.all(), empty_label=None)
    labor_hours_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=1.00)
    labor_hours = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00)
    can_delete = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('labor_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'


BidLaborHoursFormSet = formset_factory(
    BidLaborHoursForm, extra=0, formset=forms.BaseFormSet, min_num=1)


class BidTravelHoursForm(forms.Form):
    travel_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    travel_type = forms.ChoiceField(
        choices=TravelHours.TRAVEL_HOURS_CHOICES)
    travel_rate = forms.ModelChoiceField(
        queryset=Rate.objects.all(), empty_label=None)
    travel_hours_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=1.00)
    travel_hours = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00)
    can_delete = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('travel_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'


BidTravelHoursFormSet = formset_factory(
    BidTravelHoursForm, extra=0, formset=forms.BaseFormSet, min_num=1)


class BidTravelExpenseForm(forms.Form):
    travel_expense_id = forms.IntegerField(
        required=False, widget=forms.HiddenInput())
    expense_type = forms.ChoiceField(
        choices=TravelExpense.EXPENSE_TYPE_CHOICES)
    expense_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=1.00)
    expense_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.0)
    can_delete = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('travel_expense_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'


BidTravelExpenseFormSet = formset_factory(
    BidTravelExpenseForm, extra=0, formset=forms.BaseFormSet, min_num=1)
