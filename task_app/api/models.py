# 1. Third-party suppliers
from django.db import models
from django.contrib.auth.models import User

# 2. Local imports
from board_app.api.models import Board


class Task(models.Model):
    """
    A task that belongs to a board, has an assignee, reviewer, and status.
    """
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
        Board, on_delete=models.CASCADE, related_name='tasks', verbose_name='Board'
    )
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='to-do', verbose_name='Status'
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='low', verbose_name='Priority'
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name='Assignee'
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks', verbose_name='Reviewer'
    )
    due_date = models.DateField(null=True, blank=True, verbose_name='Due Date')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='Created By'
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def create(self, validated_data):
        """
        Create a new task instance.
        """
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        assignee = User.objects.filter(
            id=assignee_id).first() if assignee_id else None
        reviewer = User.objects.filter(
            id=reviewer_id).first() if reviewer_id else None

        user = self.context['request'].user
        validated_data['created_by'] = user

        task = Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )
        return task

    def __str__(self):
        """
        Return a string representation of the task with its title and status.
        """
        return f"{self.title} ({self.status})"


class Comment(models.Model):
    """
    A comment associated with a task, authored by a user.
    """
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments', verbose_name='Task'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='Author')
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created At')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """
        Return a string representation of the comment, showing the author and the creation date.
        """
        return f"Comment by {self.author} on {self.created_at}"
