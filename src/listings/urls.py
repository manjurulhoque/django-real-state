from django.contrib import admin
from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.ListingsListView.as_view(), name='listings'),
    path('search', views.search, name='search'),
    path('<slug:listing_id>', views.ListingDetailView.as_view(), name='listing'),
]
