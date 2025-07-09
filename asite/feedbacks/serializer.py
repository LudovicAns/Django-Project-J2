from rest_framework import serializers
from .models import Feedbacks


class FeedbackSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = Feedbacks
        fields = ['id', 'job', 'author_name', 'comment', 'rating', 'created_at']