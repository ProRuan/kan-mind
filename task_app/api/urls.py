from django.urls import path
from .views import TaskCreateView, AssignedToMeTasksView, ReviewingTasksView

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('assigned-to-me/', AssignedToMeTasksView.as_view(), name='assigned-to-me'),
    path('reviewing/', ReviewingTasksView.as_view(), name='reviewing-tasks'),
]
