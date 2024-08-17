from rest_framework.serializers import ModelSerializer
from .models import Timeline


class TimelineSerializer(ModelSerializer):
    class Meta:
        model = Timeline
        fields = "__all__"
