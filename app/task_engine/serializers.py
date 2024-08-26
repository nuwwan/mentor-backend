from rest_framework.serializers import ModelSerializer
from .models import Timeline, Tag


class TimelineSerializer(ModelSerializer):
    class Meta:
        model = Timeline
        fields = "__all__"
        read_only_fields = ["user"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["author"]
