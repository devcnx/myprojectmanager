from django.urls import path
from . import views


app_name = 'bid'
urlpatterns = [
    path('bid_sheets/', views.IndexView.as_view(), name='index'),
    path('bid_sheet_details/<int:pk>/',
         views.BidDetailView.as_view(), name='bid_details'),
]
