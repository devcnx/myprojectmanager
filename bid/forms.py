from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('created_on', 'created_by',
                   'last_updated_on', 'last_updated_by')
