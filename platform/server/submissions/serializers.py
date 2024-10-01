from rest_framework import serializers
from .models import Submission, Review, ReviewRequest
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SubmissionSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        many=True
    )
    reviewers = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_reviewer=True), 
        many=True, 
        required=False
    )

    class Meta:
        model = Submission
        fields = [
            'id', 
            'title', 
            'abstract', 
            'content_file',
            'submission_date', 
            'authors', 
            'reviewers', 
            'review_status', 
            'categories'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'submission', 'content', 'reviewed_at']
        read_only_fields = ['reviewer', 'submission', 'reviewed_at']

class ReviewRequestSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    class Meta:
        model = ReviewRequest
        fields = ['id', 'reviewer', 'submission', 'status', 'requested_at',]
        read_only_fields = ['reviewer', 'submission', 'status', 'requested_at',]