# 1. Third-party imports
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 2. Local imports
from .serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardOverviewSerializer,
    BoardUpdateSerializer,
)
from board_app.models import Board
from task_app.models import Task


class BoardListCreateView(APIView):
    """
    API view to retrieve a list of boards the user belongs to or owns,
    and to create a new board.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return all boards where the user is a member or the owner.

        Returns:
            Response: A list of serialized boards.
        """
        user = request.user
        boards = Board.objects.filter(
            members=user) | Board.objects.filter(owner=user)
        boards = boards.distinct()
        serializer = BoardOverviewSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new board with the current user as the owner.

        Returns:
            Response: The created board in overview format or validation errors.
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
    API view to retrieve, update, or delete a specific board.
    """
    permission_classes = [IsAuthenticated]

    def get_board(self, board_id, user):
        """
        Fetch the board if the user is authorized.

        Args:
            board_id (int): ID of the board.
            user (User): Authenticated user.

        Returns:
            Board or None: The board object if authorized, otherwise None.
        """
        board = get_object_or_404(Board, id=board_id)
        if user != board.owner and user not in board.members.all():
            return None
        return board

    def get(self, request, board_id):
        """
        Retrieve full board details including members and tasks.

        Returns:
            Response: Serialized board details or 403 if unauthorized.
        """
        board = self.get_board(board_id, request.user)
        if not board:
            return self._get_permission_response()

        tasks = Task.objects.filter(board=board)
        serializer = BoardDetailSerializer(board, context={'tasks': tasks})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, board_id):
        """
        Partially update board title or members.

        Only accessible by board owner or members.

        Returns:
            Response: Serialized updated board or 403 if unauthorized.
        """
        board = self.get_board(board_id, request.user)
        if not board:
            return self._get_permission_response()

        serializer = BoardUpdateSerializer(
            board, data=request.data, partial=True
        )
        if serializer.is_valid():
            return self._get_success_response(serializer)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id):
        """
        Delete the specified board.

        Only the owner is allowed to delete a board.

        Returns:
            Response: 204 No Content on success, 403 if unauthorized.
        """
        board = get_object_or_404(Board, id=board_id)
        if board.owner != request.user:
            return Response(
                {"detail": "Only the board owner can delete this board."},
                status=status.HTTP_403_FORBIDDEN
            )

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_permission_response(self):
        """
        Return a standard permission denied response.

        Returns:
            Response: 403 Forbidden.
        """
        return Response(
            {"detail": "You do not have permission to access or modify this board."},
            status=status.HTTP_403_FORBIDDEN
        )

    def _get_success_response(self, serializer):
        """
        Return the successful update response.

        Args:
            serializer (Serializer): A valid serializer instance.

        Returns:
            Response: Serialized updated board data.
        """
        updated_board = serializer.save()
        return Response(
            BoardUpdateSerializer(updated_board).data,
            status=status.HTTP_200_OK
        )
