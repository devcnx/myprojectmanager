from django import forms
from projects.models import Project
from .models import WorkOrder, WorkOrderTrip


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        # Set the value of the work order number field to the value returned by the get_next_work_order_number() method
        widgets = {
            'work_order_number': forms.TextInput(attrs={'value': WorkOrder.get_next_work_order_number(), 'readonly': 'readonly'}),
            'work_order_project': forms.Select(attrs={'readonly': 'readonly'}),
            'work_order_site': forms.Select(attrs={'readonly': 'readonly'}),
        }


class WorkOrderTripForm(forms.ModelForm):
    class Meta:
        model = WorkOrderTrip
        fields = '__all__'
