"""
URL configuration for board-related endpoints.
Defines URL patterns for listing, creating,
retrieving, updating, and deleting boards.

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
