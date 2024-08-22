from rest_framework.serializers import ModelSerializer
from .models import Timeline


class TimelineSerializer(ModelSerializer):
    class Meta:
        model = Timeline
        fields = "__all__"
        read_only_fields = ["user"]
