from django.urls import path
from . import views


app_name = 'materials'
urlpatterns = [
    path('add_material/', views.AddMaterialTemplateView.as_view(), name='add_material'),
]
