"""
Serializers for task_app.

This module provides serializers for Task, Comment, and User summary representations,
including creation and validation logic for tasks.
"""

# 1. Third-party suppliers
from django.contrib.auth.models import User
from rest_framework import serializers

# 2. Local imports
from .models import Task, Board, Comment


class UserSummarySerializer(serializers.ModelSerializer):
    """Serializer for summarizing User data."""
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Task, including user IDs for assignee and reviewer.
    Performs board membership validation.
    """
    assignee_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    reviewer_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    assignee = UserSummarySerializer(read_only=True)
    reviewer = UserSummarySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee_id', 'reviewer_id', 'assignee', 'reviewer',
            'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, 'comments') else 0

    def validate(self, data):
        user = self.context['request'].user
        board = data.get('board')
        assignee_id = data.get('assignee_id')
        reviewer_id = data.get('reviewer_id')

        def is_member(user_id):
            return board.members.filter(id=user_id).exists()

        if not is_member(user.id):
            raise serializers.ValidationError(
                "You are not a member of this board.")
        if assignee_id and not is_member(assignee_id):
            raise serializers.ValidationError(
                "Assignee must be a member of the board.")
        if reviewer_id and not is_member(reviewer_id):
            raise serializers.ValidationError(
                "Reviewer must be a member of the board.")

        return data

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        assignee = User.objects.filter(
            id=assignee_id).first() if assignee_id else None
        reviewer = User.objects.filter(
            id=reviewer_id).first() if reviewer_id else None

        validated_data['created_by'] = self.context['request'].user

        return Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )


class UserShortSerializer(serializers.ModelSerializer):
    """Short version of user serializer with full name."""
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Task including assignee, reviewer, and comment count.
    """
    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for task comments."""
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}".strip()
