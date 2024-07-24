from rest_framework.serializers import ModelSerializer
from .models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "base_user",
            "is_mentee",
            "is_mentor",
            "title",
            "gender",
            "birth_year",
            "birth_month",
            "birth_date",
            "country_origin",
            "country_live",
            "age",
            "profile_photo",
        ]
