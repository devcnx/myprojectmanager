from django.urls import path
from . import views


app_name = 'customers'
urlpatterns = [
    path('new_customer_contact/', views.new_customer_contact,
         name='new_customer_contact'),
]
