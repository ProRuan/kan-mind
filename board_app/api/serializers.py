from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Board


class BoardOverviewSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id')

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'member_count',
                  'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']

    def get_member_count(self, board):
        return board.members.count()

    def get_ticket_count(self, board):
        return board.tasks.count()

    def get_tasks_to_do_count(self, board):
        return board.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, board):
        return board.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Board
        fields = ['title', 'members']

    def create(self, validated_data):
        members = validated_data.pop('members')
        owner = self.context['request'].user
        board = Board.objects.create(owner=owner, **validated_data)
        board.members.set(members)
        return board
