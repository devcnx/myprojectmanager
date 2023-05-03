from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Customer, CustomerContact


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = '__all__'
        # exclude = ('added_by', 'last_updated_by')
