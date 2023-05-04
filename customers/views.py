""" 
Views for the Customer App
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import CustomerContactForm
from .models import CustomerContact


@login_required
def new_customer_contact(request):
    """ 
    View for handling the creation of a new customer contact.
    """
    if request.method == 'POST':
        form = CustomerContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.added_by = request.user
            contact.last_updated_by = request.user
            contact.save()
            return JsonResponse({
                'success': True,
                'customer_contact_id': contact.pk,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'work_phone': contact.work_phone,
                'cell_phone': contact.cell_phone,
                'email': contact.email,
            })
        else:
            form_html = render_to_string(
                'customers/customer_contact_form.html',
                {'form': form},
                request=request,
            )
            return JsonResponse({
                'success': False,
                'form_html': form_html,
            })
    else:
        form = CustomerContactForm()
        form_html = render_to_string(
            'customers/customer_contact_form.html',
            {'form': form},
            request=request,
        )
        return JsonResponse({
            'success': True,
            'form_html': form_html,
        })
