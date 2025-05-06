# test 1
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Board
from .serializers import BoardSerializer


# delete!
@api_view(['GET'])
def board_test_view(request):
    return Response({'request': 'board test view works'})


class BoardListView(APIView):

    def get(self, request):
        # Retrieve all boards
        boards = Board.objects.all()

        # Serialize the boards
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
