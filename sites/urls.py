from django.urls import path
from . import views


app_name = 'sites'
urlpatterns = [
    path('add_new_site/', views.add_new_site, name='add_new_site'),
]
