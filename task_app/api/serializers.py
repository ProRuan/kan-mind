from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Board, Comment


class UserSummarySerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True)
    reviewer_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True)
    assignee = UserSummarySerializer(read_only=True)
    reviewer = UserSummarySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description',
            'status', 'priority', 'assignee_id', 'reviewer_id',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        return 0  # Replace with real logic if you add comments later

    def validate(self, data):
        user = self.context['request'].user
        board = data.get('board')
        assignee_id = data.get('assignee_id')
        reviewer_id = data.get('reviewer_id')

        # check this!
        # Check user is in board
        if not board.members.filter(id=user.id).exists():
            raise serializers.ValidationError(
                "Du bist kein Mitglied dieses Boards.")

        # check this!
        # Check assignee and reviewer are in board
        if assignee_id and not board.members.filter(id=assignee_id).exists():
            raise serializers.ValidationError(
                "Assignee muss Mitglied des Boards sein.")
        if reviewer_id and not board.members.filter(id=reviewer_id).exists():
            raise serializers.ValidationError(
                "Reviewer muss Mitglied des Boards sein.")

        return data

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        assignee = User.objects.filter(
            id=assignee_id).first() if assignee_id else None
        reviewer = User.objects.filter(
            id=reviewer_id).first() if reviewer_id else None

        task = Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )
        return task


# GET
class UserShortSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}".strip()
