from django.urls import path
from . import views


app_name = 'customers'
urlpatterns = [
    # Path used to dynamically load the form to create a new customer contact. 
    path('new_customer_contact/', views.new_customer_contact,
         name='new_customer_contact'),
]
