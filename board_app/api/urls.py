"""
URL configuration for the board-related endpoints.

This module defines the URL patterns for listing, creating, retrieving,
updating, and deleting boards. It uses Django's path() function to map
requests to class-based views.

Namespace:
    board_app

Available endpoints:
    - / → BoardListCreateView
    - /<int:board_id>/ → BoardDetailView
"""

# 1. Third-party imports
from django.urls import path

# 2. Local imports
from .views import BoardDetailView, BoardListCreateView

app_name = 'board_app'

urlpatterns = [
    path('', BoardListCreateView.as_view(), name='board-list-create'),
    path('<int:board_id>/', BoardDetailView.as_view(), name='board-detail'),
]
