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


# check owners and members ...

# Please check the validation, set proper default values, set required (if necessary), do clean coding, documentate according to PEP8 and replace German error texts with English error texts, please:

# DELETE and MOVE!!!

# auth_app (1/3) ...
# --------
# errors (0/0) - check
# validation, default, required (0/3) ...
# clean coding and documentation (0/2) ...
# English error texts (0/1) ...


# clean coding (1/3) ...


# for copying
# -----------
# errors (0/?) ...
# validation, default, required (0/3) ...
# clean coding and documentation (0/2) ...
# English error texts (0/1) ...
