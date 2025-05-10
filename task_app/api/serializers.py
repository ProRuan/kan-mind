# 1. Third-party imports
from django.contrib.auth.models import User
from rest_framework import serializers

# 2. Local imports
from task_app.models import Task, Comment


class UserSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for summarizing User data with full name.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Return the user's full name.
        """
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Task, including assignee and reviewer IDs.
    Also returns related assignee/reviewer summary data.
    """
    assignee_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        write_only=True
    )
    reviewer_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        write_only=True
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
        """
        Return the number of comments associated with this task.
        """
        return obj.comments.count() if hasattr(obj, 'comments') else 0

    def validate(self, data):
        """
        Validate that all involved users are members of the board.
        """
        user = self.context['request'].user
        board = data.get('board')

        self._validate_board_membership(
            board,
            creator_id=user.id,
            assignee_id=data.get('assignee_id'),
            reviewer_id=data.get('reviewer_id')
        )
        return data

    def _validate_board_membership(self, board, creator_id, assignee_id, reviewer_id):
        """
        Ensure that the creator, assignee, and reviewer are board members.
        """
        checks = [
            (creator_id, "You are not a member of this board."),
            (assignee_id, "Assignee must be a member of the board."),
            (reviewer_id, "Reviewer must be a member of the board."),
        ]

        for user_id, error_msg in checks:
            if user_id and not board.members.filter(id=user_id).exists():
                raise serializers.ValidationError(error_msg)

    def create(self, validated_data):
        """
        Create a Task instance with assignee and reviewer if provided.
        """
        assignee = self._get_user_from_id(
            validated_data.pop('assignee_id', None)
        )
        reviewer = self._get_user_from_id(
            validated_data.pop('reviewer_id', None)
        )
        validated_data['created_by'] = self.context['request'].user

        return Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )

    def _get_user_from_id(self, user_id):
        """
        Fetch a user instance by ID.
        """
        return User.objects.filter(id=user_id).first() if user_id else None


class UserShortSerializer(serializers.ModelSerializer):
    """
    Compact user serializer used for read-only task display.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Return the user's full name.
        """
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskSerializer(serializers.ModelSerializer):
    """
    Read-only Task serializer with assignee, reviewer, and comment count.
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
        """
        Return the number of comments on the task.
        """
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments on tasks, including author name.
    """
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']

    def get_author(self, obj):
        """
        Return the comment author's full name.
        """
        return f"{obj.author.first_name} {obj.author.last_name}".strip()
