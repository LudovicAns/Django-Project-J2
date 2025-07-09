from rest_framework import serializers
from .models import Feedback
from ..jobs.serializer import JobRecordSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    job = JobRecordSerializer(read_only=True)
    author_name = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = Feedback
        fields = ['id', 'job', 'author_name', 'comment', 'rating', 'created_at']