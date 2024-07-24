from django.urls import path
from .views import ProfileDetail, ProfileList
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("profiles/", ProfileList.as_view(), name="profile_list"),
    path("profiles/<int:pk>/", ProfileDetail.as_view(), name="profile_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
