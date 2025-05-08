from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from .models import Board
from task_app.api.models import Task
from .serializers import BoardCreateSerializer, BoardOverviewSerializer
from board_app.api.serializers import (
    BoardDetailSerializer,
    BoardUpdateSerializer
)


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


class BoardDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_board(self, board_id, user):
        board = get_object_or_404(Board, id=board_id)
        if user != board.owner and user not in board.members.all():
            return None
        return board

    def get(self, request, board_id):
        board = self.get_board(board_id, request.user)
        if not board:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        tasks = Task.objects.filter(board=board)
        serializer = BoardDetailSerializer(board, context={'tasks': tasks})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, board_id):
        board = self.get_board(board_id, request.user)
        if not board:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer = BoardUpdateSerializer(
            board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        if board.owner != request.user:
            return Response({"detail": "Only the owner can delete the board."}, status=status.HTTP_403_FORBIDDEN)

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
