from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from ..serializers import TimelineSerializer
from ..models import Timeline, Mentorship

AuthUser = get_user_model()


# Get all Timelines for a user
class TimelinesList(generics.ListCreateAPIView):
    serializer_class = TimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Timeline.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Timeline details view
class TimelineDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Timeline.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


"""
Get all timelines a mentor is asigned for.
"""


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


"""
Add Mentor for a timeline.
@param mentor : mentor id
@param timeline : timeline id
@param subject : subject 
"""


class AssignTimelineToMentor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        payload = request.data
        try:
            timeline_id = payload.get("timeline", None)
            mentor_id = payload.get("mentor", None)
            subject = payload.get("subject", None)

            mentor = AuthUser.objects.get(id=mentor_id)
            timeline = Timeline.objects.get(id=timeline_id)
            if mentor is None:
                return Response(
                    data={"message": "Mentor does not Exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if timeline is None:
                return Response(
                    data={"message": "Timeline does not Exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            mentorship = Mentorship.objects.get_or_create(
                mentor=mentor,
                mentee=logged_in_user,
                timeline=timeline,
                subject=subject,
            )
            return Response(
                data={
                    "message": "Successfully created",
                    "mentorship": mentorship[0].id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as ex:
            return Response(
                data={"message": "Internal server Error!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
