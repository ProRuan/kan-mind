"""
URL configuration for authentication-related endpoints.
Defines URL patterns for user registration, login, and email checking.

Available endpoints:
    - /registration/ → RegistrationView
    - /login/ → LoginView
    - /email-check/ → EmailCheckView
"""

# 1. Third-party suppliers
from django.urls import path

# 2. Local imports
from .views import EmailCheckView, LoginView, RegistrationView

app_name = 'auth_app'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
