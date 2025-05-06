from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    # member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    # add owner_id and member_count?
    class Meta:
        model = Board
        fields = ['id', 'title',
                  'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']

    # def get_member_count(self, obj):
    #     return obj.members.count()  # Assuming you have a many-to-many field for members

    def get_ticket_count(self, obj):
        return obj.tasks.count()  # Assuming each board has tasks

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to_do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
