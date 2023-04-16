from django.urls import path
from . import views

app_name = 'work_orders'
urlpatterns = [
    path('work_order/<int:pk>/', views.WorkOrderDetailView.as_view(),
         name='work_order_details'),
]
