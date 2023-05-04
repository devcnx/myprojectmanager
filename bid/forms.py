import datetime
from django import forms
from django.forms import formset_factory, modelformset_factory, ModelForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from equipment.models import Equipment
from labor.models import LaborHours
from rates.models import Rate
from travel.models import TravelHours, TravelExpense
from .models import Bid, BidMaterial, BidEquipment


class AdminBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('created_on', 'created_by',
                   'last_updated_on', 'last_updated_by')


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        readonly_fields = ('bid_project',)
        exclude = ('bid_submitted', 'bid_submitted_by', 'bid_labor_hours', 'bid_travel_hours',
                   'bid_travel_expenses', 'bid_materials', 'bid_equipment',
                   'created_on', 'created_by', 'last_updated_on', 'last_updated_by')
        widgets = {
            'bid_due_date': forms.DateInput(attrs={'type': 'date', 'value': datetime.date.today()}),
            'bid_due_time': forms.TimeInput(attrs={'type': 'time', 'value': datetime.datetime.now().strftime('%H:%M')}),
        }


class BidLaborHoursForm(forms.Form):
    labor_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    labor_type = forms.ChoiceField(
        choices=LaborHours.LABOR_HOURS_CHOICES, label='Labor Type')
    labor_rate = forms.ModelChoiceField(
        queryset=Rate.objects.all(), label='Labor Rate', empty_label=None)
    labor_hours_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00, label='# of Days/Nights')
    labor_hours = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00, label='Hours Per Day/Night')
    can_delete = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(BidLaborHoursForm, self).__init__(*args, **kwargs)
        if self.initial.get('labor_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'


BidLaborHoursFormSet = formset_factory(
    BidLaborHoursForm, extra=0, formset=forms.BaseFormSet, min_num=0)


class BidTravelHoursForm(forms.Form):
    travel_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    travel_type = forms.ChoiceField(
        choices=TravelHours.TRAVEL_HOURS_CHOICES, label='Travel Type')
    travel_rate = forms.ModelChoiceField(
        queryset=Rate.objects.all(), label='Travel Rate', empty_label=None)
    travel_hours_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00, label='# of Days/Nights')
    travel_hours = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00, label='Hours Per Day/Night')
    can_delete = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('travel_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'


BidTravelHoursFormSet = formset_factory(
    BidTravelHoursForm, extra=0, formset=forms.BaseFormSet, min_num=0)


class BidTravelExpenseForm(forms.Form):
    travel_expense_id = forms.IntegerField(
        required=False, widget=forms.HiddenInput())
    expense_type = forms.ChoiceField(
        choices=TravelExpense.EXPENSE_TYPE_CHOICES, label='Expense Type')
    expense_quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00, label='Quantity')
    expense_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00, label='Amount')
    can_delete = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('travel_expense_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'


BidTravelExpenseFormSet = formset_factory(
    BidTravelExpenseForm, extra=0, formset=forms.BaseFormSet, min_num=0)


class BidMaterialForm(forms.ModelForm):
    class Meta:
        model = BidMaterial
        fields = '__all__'


class BidEquipmentForm(forms.Form):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(), empty_label=None)
    quantity = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=1.00)
    unit_price = forms.DecimalField(
        max_digits=10, decimal_places=2, initial=0.00)
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'value': datetime.date.today(),
        })
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'value': datetime.datetime.now().strftime('%H:%M'),
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'value': datetime.date.today(),
        })
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'value': datetime.datetime.now().strftime('%H:%M'),
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('bid_id'):
            self.fields['can_delete'].widget = forms.CheckboxInput()
            self.fields['can_delete'].label = 'Delete'
            self.fields['can_delete'].attrs


BidEquipmentFormSet = formset_factory(
    BidEquipmentForm, extra=0, formset=forms.BaseFormSet, min_num=0, can_delete=True)


# class BidEquipmentForm(forms.ModelForm):
#     class Meta:
#         model = BidEquipment
#         fields = '__all__'
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().strftime('%m/%d/%Y')}),
#             'start_time': forms.TimeInput(attrs={'type': 'time', 'value': timezone.now().strftime('%H:%M')}),
#             'end_date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().strftime('%m/%d/%Y')}),
#             'end_time': forms.TimeInput(attrs={'type': 'time', 'value': timezone.now().strftime('%H:%M')}),
#         }

#         labels = {
#             'equipment': 'Equipment',
#             'start_date': 'Start Date',
#             'start_time': 'Start Time',
#             'end_date': 'End Date',
#             'end_time': 'End Time',
#             'quantity': 'Quantity',
#             'unit_price': 'Unit Price',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.initial.get('id'):
#             self.fields['can_delete'].widget = forms.CheckboxInput()
#             self.fields['can_delete'].label = 'Delete'

#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get("start_date")
#         start_time = cleaned_data.get("start_time")
#         end_date = cleaned_data.get("end_date")
#         end_time = cleaned_data.get("end_time")
#         if start_date and end_date:
#             if start_date > end_date:
#                 raise forms.ValidationError(
#                     "End date should be greater than start date.")
#             elif start_date == end_date:
#                 if start_time > end_time:
#                     raise forms.ValidationError(
#                         "End time should be greater than start time.")
#         return cleaned_data


# BidEquipmentFormSet = formset_factory(
#     BidEquipmentForm, extra=0, formset=forms.BaseFormSet, min_num=0, can_delete=True)
