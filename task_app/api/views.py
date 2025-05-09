# 1. Third-party suppliers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# 2. Local imports
from .models import Task, Comment
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    CommentSerializer
)


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
        """
        Helper function to retrieve a task by ID.
        """
        return get_object_or_404(Task, id=task_id)

    def patch(self, request, task_id):
        """
        Partially update a task.
        """
        task = self.get_task(task_id)

        if request.user not in task.board.members.all():
            return Response({"detail": "You are not a member of this board."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        # Check if board ID is being modified
        if "board" in data and str(data["board"]) != str(task.board.id):
            return Response({"detail": "Board ID cannot be changed."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle assignee update
        assignee_id = data.get("assignee_id")
        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                if assignee not in task.board.members.all():
                    return Response({"detail": "Assignee must be a member of the board."}, status=status.HTTP_400_BAD_REQUEST)
                task.assignee = assignee
            except User.DoesNotExist:
                return Response({"detail": "Assignee not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle reviewer update
        reviewer_id = data.get("reviewer_id")
        if reviewer_id:
            try:
                reviewer = User.objects.get(id=reviewer_id)
                if reviewer not in task.board.members.all():
                    return Response({"detail": "Reviewer must be a member of the board."}, status=status.HTTP_400_BAD_REQUEST)
                task.reviewer = reviewer
            except User.DoesNotExist:
                return Response({"detail": "Reviewer not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated task
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        """
        Delete a task.
        """
        task = self.get_task(task_id)

        if task.created_by != request.user and task.board.owner != request.user:
            return Response({"detail": "Only the task creator or board owner can delete the task."}, status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCommentsView(APIView):
    """
    API view to retrieve and create comments for a task.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        """
        Retrieve all comments for a task.
        """
        task = get_object_or_404(Task, id=task_id)

        if request.user not in task.board.members.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        comments = task.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        """
        Add a new comment to a task.
        """
        task = get_object_or_404(Task, id=task_id)

        if request.user not in task.board.members.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content', '').strip()
        if not content:
            return Response({'detail': 'Content cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            task=task,
            author=request.user,
            content=content
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(APIView):
    """
    API view to delete a comment on a task.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        """
        Delete a comment.
        """
        task = get_object_or_404(Task, id=task_id)
        comment = get_object_or_404(Comment, id=comment_id, task=task)

        if comment.author != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
