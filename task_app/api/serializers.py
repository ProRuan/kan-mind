from rest_framework import serializers
from .models import Contact, Task


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):
    assignee = ContactSerializer()
    reviewer = ContactSerializer()

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]

    # def update(self, instance, validated_data):
    #     if 'board' in validated_data:
    #         raise serializers.ValidationError(
    #             {"board": "Ändern der Board-ID ist nicht erlaubt."})
    #     return super().update(instance, validated_data)

# think about this!


class TaskOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'due_date']
