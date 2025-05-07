from django.urls import path
from .views import BoardListCreateView, BoardDetailView

# rename board_id to id!
urlpatterns = [
    path('', BoardListCreateView.as_view(), name='board-list-create'),
    path('<int:board_id>/', BoardDetailView.as_view(), name='board-detail'),
]


# check owners and members ...
