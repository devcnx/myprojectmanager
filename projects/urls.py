from django.urls import path
from . import views


app_name = 'projects'
urlpatterns = [
    path('add_project/', views.AddProjectView.as_view(), name='add_project'),
    path('project_details/<int:pk>/',
         views.ProjectDetailView.as_view(), name='project_details'),
    path('project_update/<int:pk>/',
         views.ProjectUpdateView.as_view(), name='project_update'),

]
