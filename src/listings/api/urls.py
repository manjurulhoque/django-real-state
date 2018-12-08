from django.urls import path

from . import views

urlpatterns = [
    path('listings', views.ListingsListApiView.as_view()),
    path('listings/<slug:listing_id>', views.ListingDetailView.as_view()),
    path('search', views.SearchView.as_view()),
]
