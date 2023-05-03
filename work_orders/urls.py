from django.urls import path
from . import views

app_name = 'work_orders'
urlpatterns = [
    path('work_order/<int:pk>/', views.WorkOrderDetailView.as_view(),
         name='work_order_details'),
    path('work_order/<int:pk>/add_work_order_trip/',
         views.AddWorkOrderTripView.as_view(), name='add_work_order_trip'),
]
