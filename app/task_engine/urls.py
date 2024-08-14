from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.timeline_views import TimelinesList, TimelineDetail, GetTimelinesForMentor

urlpatterns = [
    path("timeline/", TimelinesList.as_view(), name="timeline_list"),
    path("timeline/<int:pk>/", TimelineDetail.as_view(), name="timeline_detail"),
    path(
        "mentoringTimelines/",
        GetTimelinesForMentor.as_view(),
        name="get_mentoring_timeline_for_mentor",
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
