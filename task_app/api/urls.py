from django.urls import path
from .views import task_test_view, TaskListView

urlpatterns = [
    path('', task_test_view),  # delete!
    path('assigned-to-me/', TaskListView.as_view(), name='tasks-assigned-to-me'),
    path('reviewing/', TaskListView.as_view(), name='tasks-reviewing'),
]
