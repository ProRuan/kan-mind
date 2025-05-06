# test 1
from rest_framework.decorators import api_view
from rest_framework.response import Response

# test 2
from rest_framework import generics, mixins
from .models import Task
from .serializers import TaskSerializer, TaskOverviewSerializer


# class TaskListAPIView(ListAPIView):
#     queryset = Task.objects.all()

# delete!
@api_view(['GET'])
def task_test_view(request):
    return Response({'request': 'task test view works'})


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all().select_related('assignee', 'reviewer')
    serializer_class = TaskSerializer


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TasksView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskOverviewSerializer  # shows limited fields
        return TaskSerializer  # for POST (full task)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'  # because your URL uses {task_id}
