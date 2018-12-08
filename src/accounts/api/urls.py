from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .custom_claims import MyTokenObtainPairView
from . import views

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view()),
    path('dashboard/', views.dashboard),
    path('login/', MyTokenObtainPairView.as_view()),
    path('register/', views.register),
    path('token/refresh/', TokenRefreshView.as_view()),
]
