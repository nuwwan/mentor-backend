from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from task_engine.serializers import TagSerializer
from task_engine.models import Tag


class CreateTag(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        author = request.user
        serializer = TagSerializer(data={**request.data, "author": author})
        if serializer.is_valid():
            tag = serializer.save(author=author)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            data={"message": "Internal Server Error"},
            status=status.HTTP_400_BAD_REQUEST,
        )
