from django.urls import path
from . import views


app_name = 'projects'
urlpatterns = [
    path('add/', views.AddProjectView.as_view(), name='add_project'),

]
