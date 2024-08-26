from rest_framework.serializers import ModelSerializer, ValidationError
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

    def validate_title(self, value):
        # Check if a book with the given title already exists
        if Tag.objects.filter(title=value).exists():
            raise ValidationError("A book with this title already exists.")
        return value
