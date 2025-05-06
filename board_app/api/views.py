from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Board
from .serializers import BoardCreateSerializer, BoardOverviewSerializer


class BoardListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        boards = Board.objects.filter(
            members=user) | Board.objects.filter(owner=user)
        boards = boards.distinct()
        serializer = BoardOverviewSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardCreateSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            board = serializer.save()
            overview = BoardOverviewSerializer(board)
            return Response(overview.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Board
# from .serializers import BoardOverviewSerializer, BoardCreateSerializer


# class BoardListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         boards = Board.objects.filter(
#             models.Q(owner=user) | models.Q(members=user)).distinct()
#         serializer = BoardOverviewSerializer(boards, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class BoardCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = BoardCreateSerializer(
#             data=request.data, context={'request': request})
#         if serializer.is_valid():
#             board = serializer.save()
#             overview = BoardOverviewSerializer(board)
#             return Response(overview.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
