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
