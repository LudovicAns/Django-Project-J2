from rest_framework import serializers
from .models import Feedbacks


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ['id', 'job', 'author', 'comment', 'rating', 'created_at']