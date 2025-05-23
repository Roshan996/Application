# accounts/urls.py
from django.urls import path
from .views import UserRegistrationAPIView, LoginAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),

    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
