"""
Views for managing boards, including listing, creation,
detail retrieval, updating, and deletion.
"""

# 1. Third-party suppliers
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 2. Local imports
from .models import Board
from .serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardOverviewSerializer,
    BoardUpdateSerializer
)
from task_app.api.models import Task


class BoardListCreateView(APIView):
    """
    API endpoint to list all boards the user belongs to or owns,
    and to create a new board.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return all boards where the user is a member or the owner.
        """
        user = request.user
        boards = Board.objects.filter(
            members=user) | Board.objects.filter(owner=user)
        boards = boards.distinct()
        serializer = BoardOverviewSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new board. The current user will be set as the owner.
        """
        serializer = BoardCreateSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            board = serializer.save()
            overview = BoardOverviewSerializer(board)
            return Response(overview.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    """
    API endpoint to retrieve, update, or delete a specific board.
    """
    permission_classes = [IsAuthenticated]

    def get_board(self, board_id, user):
        """
        Helper method to fetch board with access check.
        """
        board = get_object_or_404(Board, id=board_id)
        if user != board.owner and user not in board.members.all():
            return None
        return board

    def get(self, request, board_id):
        """
        Retrieve full details of a board including members and tasks.
        """
        board = self.get_board(board_id, request.user)
        if not board:
            return Response(
                {"detail": "You do not have permission to access this board."},
                status=status.HTTP_403_FORBIDDEN
            )

        tasks = Task.objects.filter(board=board)
        serializer = BoardDetailSerializer(board, context={'tasks': tasks})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, board_id):
        """
        Partially update board title or members.
        Only accessible by board members or owner.
        """
        board = self.get_board(board_id, request.user)
        if not board:
            return Response(
                {"detail": "You do not have permission to update this board."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BoardUpdateSerializer(
            board, data=request.data, partial=True
        )
        if serializer.is_valid():
            updated_board = serializer.save()
            return Response(BoardUpdateSerializer(updated_board).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id):
        """
        Delete the board.
        Only the owner of the board can perform this action.
        """
        board = get_object_or_404(Board, id=board_id)
        if board.owner != request.user:
            return Response(
                {"detail": "Only the board owner can delete this board."},
                status=status.HTTP_403_FORBIDDEN
            )

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
