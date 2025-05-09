"""
URL configuration for task-related endpoints.
Defines URL patterns for creating, retrieving, and managing tasks,
including assignments, reviews, and task comments.

Available endpoints:
    - / → TaskCreateView
    - /assigned-to-me/ → AssignedToMeTasksView
    - /reviewing/ → ReviewingTasksView
    - /<int:task_id>/ → TaskDetailView
    - /<int:task_id>/comments/ → TaskCommentsView
    - /<int:task_id>/comments/<int:comment_id>/ → CommentDeleteView
"""

# 1. Third-party imports
from django.urls import path

# 2. Local imports
from .views import (
    AssignedToMeTasksView,
    CommentDeleteView,
    ReviewingTasksView,
    TaskCommentsView,
    TaskCreateView,
    TaskDetailView
)

app_name = 'task_app'

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('assigned-to-me/', AssignedToMeTasksView.as_view(), name='assigned-to-me'),
    path('reviewing/', ReviewingTasksView.as_view(), name='reviewing-tasks'),
    path('<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path(
        '<int:task_id>/comments/',
        TaskCommentsView.as_view(),
        name='task-comments'
    ),
    path(
        '<int:task_id>/comments/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='comment-delete'
    ),
]
