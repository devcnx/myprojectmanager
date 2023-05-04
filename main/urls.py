""" 
URL Configurations for the main app. 
"""

from django.urls import path
from . import views


app_name = 'main'
urlpatterns = [
    # Path to the main app's index page
    path('', views.IndexView.as_view(), name='index'),
    # Path to the main app's dashboard page
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
