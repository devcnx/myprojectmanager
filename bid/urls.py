from django.urls import path
from . import views


app_name = 'bid'
urlpatterns = [
    path('bid_sheets/', views.IndexView.as_view(), name='index'),
    path('bid_sheet_details/<int:pk>/',
         views.BidDetailView.as_view(), name='bid_details'),
    path('bid_materials/<int:pk>/',
         views.BidDetailsMaterialView.as_view(), name='bid_details_material'),
    path('bid_equipment/<int:pk>/', views.BidDetailsEquipmentView.as_view(),
         name='bid_details_equipment'),
    path('bid_materials/delete/<int:bid_id>/<int:material_id>/',
         views.delete_bid_material, name='delete_bid_material'),
]
