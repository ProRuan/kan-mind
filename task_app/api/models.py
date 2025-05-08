from django.db import models
from django.contrib.auth.models import User
from board_app.api.models import Board


class Task(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks')
    due_date = models.DateField()

    # for comments
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)  # check default=1!

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        assignee = User.objects.filter(
            id=assignee_id).first() if assignee_id else None
        reviewer = User.objects.filter(
            id=reviewer_id).first() if reviewer_id else None

        # ✅ Inject created_by from the request
        user = self.context['request'].user
        validated_data['created_by'] = user

        task = Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )
        return task

    def __str__(self):
        return f"{self.title} ({self.status})"


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
