from django.urls import path
from .views import board_test_view, BoardListView

urlpatterns = [
    # path('', board_test_view), #delete!
    path('', BoardListView.as_view(), name='board-list'),
]
