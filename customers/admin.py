""" 
Customers App Admin Configurations 
"""

from django.contrib import admin
from .models import Customer, CustomerContact


admin.site.register(Customer)
admin.site.register(CustomerContact)
