from django.contrib.auth.models import User
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics
from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer

# GET
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignedToMeTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignee=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewingTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewer=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(self, task_id):
        return get_object_or_404(Task, id=task_id)

    def patch(self, request, task_id):
        task = self.get_task(task_id)

        if request.user not in task.board.members.all():
            return Response({"detail": "Sie sind kein Mitglied dieses Boards."}, status=status.HTTP_403_FORBIDDEN)

        if "board" in request.data:
            return Response({"detail": "Die Board-ID darf nicht geändert werden."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()

        if "assignee_id" in data:
            try:
                assignee = User.objects.get(id=data["assignee_id"])
                if assignee not in task.board.members.all():
                    return Response({"detail": "Assignee ist kein Mitglied des Boards."}, status=status.HTTP_400_BAD_REQUEST)
                task.assignee = assignee
            except User.DoesNotExist:
                return Response({"detail": "Assignee nicht gefunden."}, status=status.HTTP_400_BAD_REQUEST)

        if "reviewer_id" in data:
            try:
                reviewer = User.objects.get(id=data["reviewer_id"])
                if reviewer not in task.board.members.all():
                    return Response({"detail": "Reviewer ist kein Mitglied des Boards."}, status=status.HTTP_400_BAD_REQUEST)
                task.reviewer = reviewer
            except User.DoesNotExist:
                return Response({"detail": "Reviewer nicht gefunden."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = self.get_task(task_id)

        if task.created_by != request.user and task.board.owner != request.user:
            return Response(
                {"detail": "Nur der Ersteller der Task oder der Board-Eigentümer kann sie löschen."},
                status=status.HTTP_403_FORBIDDEN
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
