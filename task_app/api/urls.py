from django.urls import path
from .views import TaskCreateView, AssignedToMeTasksView, ReviewingTasksView, TaskDetailView, TaskCommentsView, CommentDeleteView

# rename task_id to id!
urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('assigned-to-me/', AssignedToMeTasksView.as_view(), name='assigned-to-me'),
    path('reviewing/', ReviewingTasksView.as_view(), name='reviewing-tasks'),
    path('<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:task_id>/comments/',
         TaskCommentsView.as_view(), name='task-comments'),
    path('<int:task_id>/comments/<int:comment_id>/',
         CommentDeleteView.as_view(), name='comment-delete'),
]

# TaskDetailView
# --------------
# Make sure Task has the fields: assignee, reviewer, board, created_by.
# Make sure board.members and board.owner are properly set up.
# TaskSerializer must return full assignee and reviewer objects if you want the detailed response.
