# test 1
from rest_framework.decorators import api_view
from rest_framework.response import Response

# test 2
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer


# class TaskListAPIView(ListAPIView):
#     queryset = Task.objects.all()


@api_view(['GET'])
def task_test_view(request):
    return Response({'request': 'task test view works'})


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all().select_related('assignee', 'reviewer')
    serializer_class = TaskSerializer
