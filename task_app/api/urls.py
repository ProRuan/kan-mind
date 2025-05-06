from django.urls import path
from .views import TasksView, TaskListView, TaskDetailView

urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('assigned-to-me/', TaskListView.as_view(), name='tasks-assigned-to-me'),
    path('reviewing/', TaskListView.as_view(), name='tasks-reviewing'),
    path('<int:id>/', TaskDetailView.as_view(), name='task-detail'),
]
