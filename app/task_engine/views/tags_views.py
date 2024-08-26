from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from task_engine.serializers import TagSerializer
from task_engine.models import Tag


class CreateTag(APIView):
    permission_classes = [IsAuthenticated]

    """
    This Endpoint will accept a search string as title=... and 
    returns the  matching Tags whose title like the given string.
    Sesrch string should be 3 char or longer.
    """

    def get(self, request):
        try:
            search_str = request.query_params.get("title")

            if len(search_str) < 3 or search_str == None:
                return Response(
                    {"message": "search string should be 3 charcters or more"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tags = Tag.objects.filter(title__icontains=search_str).order_by("title")[:8]
            serializer = TagSerializer(tags, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, *args, **kwargs):
        author = request.user
        serializer = TagSerializer(data={**request.data, "author": author})
        if serializer.is_valid():
            tag = serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
