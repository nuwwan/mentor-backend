from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.timeline_views import (
    TimelinesList,
    TimelineDetail,
    GetTimelinesForMentor,
    AssignTimelineToMentor,
)
from .views.tags_views import CreateTag

urlpatterns = [
    path("timeline/", TimelinesList.as_view(), name="timeline_list"),
    path("timeline/<int:pk>/", TimelineDetail.as_view(), name="timeline_detail"),
    path(
        "mentoringTimelines/",
        GetTimelinesForMentor.as_view(),
        name="get_mentoring_timeline_for_mentor",
    ),
    path(
        "add_mentor_to_timeline/",
        AssignTimelineToMentor.as_view(),
        name="add_mentor_to_timeline",
    ),
    path("tag/", CreateTag.as_view(), name="tag_list"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
