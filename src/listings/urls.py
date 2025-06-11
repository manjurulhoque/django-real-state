from django.contrib import admin
from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.ListingsListView.as_view(), name='listings'),
    path('for-sale/', views.SaleListingsView.as_view(), name='for_sale'),
    path('for-rent/', views.RentListingsView.as_view(), name='for_rent'),
    path('search', views.search, name='search'),
    path('submit/', views.submit_listing, name='submit_listing'),
    path('edit/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('<slug:listing_id>', views.ListingDetailView.as_view(), name='listing'),
]
