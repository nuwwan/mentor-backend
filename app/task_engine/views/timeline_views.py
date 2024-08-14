from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import TimelineSerializer
from ..models import Timeline, Mentorship


# Get all Timelines for a user
class TimelinesList(generics.ListCreateAPIView):
    serializer_class = TimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Timeline.objects.filter(user=self.request.user)


# Timeline details view
class TimelineDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Timeline.objects.filter(user=self.request.user)


class GetTimelinesForMentor(APIView):
    def get(self, request, *args, **kwargs):
        try:
            mentorships = Mentorship.objects.filter(mentor=request.user)
            timelines = [m.timeline for m in mentorships]
            parsed_data = TimelineSerializer(timelines, many=True)
            return Response(data=parsed_data.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                data={"message": "Operation Failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
