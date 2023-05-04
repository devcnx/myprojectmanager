from django import forms
""" 
Customers App Forms

Forms :
    CustomerContactForm - Form for adding/editing customer contacts.
"""

from .models import CustomerContact


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = '__all__'
        exclude = ('added_by', 'last_updated_by')
