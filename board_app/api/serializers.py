# 1. Third-party suppliers
from django.contrib.auth.models import User
from rest_framework import serializers

# 2. Local imports
from board_app.models import Board
from task_app.models import Task


class BoardOverviewSerializer(serializers.ModelSerializer):
    """
    Overview serializer showing board summary statistics.
    """
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id')

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'owner_id', 'member_count',
            'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count'
        ]

    def get_member_count(self, board):
        return board.members.count()

    def get_ticket_count(self, board):
        return board.tasks.count()

    def get_tasks_to_do_count(self, board):
        return board.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, board):
        return board.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new board.
    """
    title = serializers.CharField(required=True, max_length=255)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=True
    )

    class Meta:
        model = Board
        fields = ['title', 'members']

    def create(self, validated_data):
        members = validated_data.pop('members')
        owner = self.context['request'].user
        board = Board.objects.create(owner=owner, **validated_data)
        board.members.set(members)
        return board


class UserShortSerializer(serializers.ModelSerializer):
    """
    Short user serializer with ID, email and full name.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for listing tasks in a board.
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


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Full board detail view including members and tasks.
    """
    members = UserShortSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']

    def get_tasks(self, obj):
        tasks = self.context.get('tasks', Task.objects.filter(board=obj))
        return TaskSerializer(tasks, many=True).data


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a board.
    """
    title = serializers.CharField(
        required=False, allow_blank=False, max_length=255)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'members']

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        if members is not None:
            instance.members.set(members)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'owner_data': UserShortSerializer(instance.owner).data,
            'members_data': UserShortSerializer(instance.members.all(), many=True).data
        }
