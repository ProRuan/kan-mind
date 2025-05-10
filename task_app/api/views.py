# 1. Third-party suppliers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 2. Local imports
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    CommentSerializer
)
from task_app.models import Comment, Task


class TaskCreateView(generics.CreateAPIView):
    """
    API view to create a new task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignedToMeTasksView(APIView):
    """
    API view to retrieve tasks assigned to the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignee=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewingTasksView(APIView):
    """
    API view to retrieve tasks that the authenticated user is reviewing.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewer=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskDetailView(APIView):
    """
    API view to retrieve, update or delete a task.
    """
    permission_classes = [IsAuthenticated]

    def get_task(self, task_id):
        return get_object_or_404(Task, id=task_id)

    def patch(self, request, task_id):
        task = self.get_task(task_id)
        if not self._is_board_member(request.user, task.board):
            return self._error("You are not a member of this board.", 403)

        data = request.data.copy()
        if self._board_changed(data, task):
            return self._error("Board ID cannot be changed.")

        for role in [("assignee_id", "assignee"), ("reviewer_id", "reviewer")]:
            if error := self._update_user_field(data, task, *role):
                return error

        return self._save_task(task, data)

    def _is_board_member(self, user, board):
        return board.members.filter(id=user.id).exists()

    def _board_changed(self, data, task):
        return "board" in data and str(data["board"]) != str(task.board.id)

    def _update_user_field(self, data, task, field_key, attr_name):
        user_id = data.get(field_key)
        if not user_id:
            return None

        user = self._get_user_or_error(user_id, attr_name)
        if isinstance(user, Response):
            return user

        if not self._is_board_member(user, task.board):
            return self._error(f"{attr_name.capitalize()} must be a member of the board.")

        setattr(task, attr_name, user)
        return None

    def _get_user_or_error(self, user_id, role):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return self._error(f"{role.capitalize()} not found.")

    def _save_task(self, task, data):
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _error(self, message, status_code=400):
        return Response({"detail": message}, status=status_code)

    def delete(self, request, task_id):
        task = self.get_task(task_id)

        if task.created_by != request.user and task.board.owner != request.user:
            return Response(
                {"detail": "Only the task creator or board owner can delete the task."},
                status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCommentsView(APIView):
    """
    API view to retrieve and create comments for a task.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user not in task.board.members.all():
            return Response(
                {'detail': 'Forbidden'},
                status=status.HTTP_403_FORBIDDEN)

        comments = task.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if not self._is_board_member(request.user, task.board):
            return self._error('Forbidden', 403)

        content = self._get_content(request)
        if not content:
            return self._error('Content cannot be empty.')

        comment = self._create_comment(task, request.user, content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _is_board_member(self, user, board):
        return board.members.filter(id=user.id).exists()

    def _error(self, message, status_code=400):
        return Response({'detail': message}, status=status_code)

    def _get_content(self, request):
        return request.data.get('content', '').strip()

    def _create_comment(self, task, user, content):
        return Comment.objects.create(task=task, author=user, content=content)


class CommentDeleteView(APIView):
    """
    API view to delete a comment on a task.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        task = get_object_or_404(Task, id=task_id)
        comment = get_object_or_404(Comment, id=comment_id, task=task)

        if comment.author != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
