# 1. Third-party suppliers
from django.db import models
from django.contrib.auth.models import User

# 2. Local imports
from board_app.models import Board


class Task(models.Model):
    """
    Represents a task associated with a specific board.

    A task includes metadata such as status, priority, assignee,
    reviewer, due date, and the user who created it.
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
        Board,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Board'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        default=''
    )
    description = models.TextField(
        max_length=510,
        verbose_name='Description',
        blank=True,
        default=''
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='to-do',
        verbose_name='Status'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='low',
        verbose_name='Priority'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Assignee'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_tasks',
        verbose_name='Reviewer'
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Due Date'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Created By'
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def create(self, validated_data):
        """
        Creates and returns a Task instance using validated data.

        Looks up optional assignee and reviewer by ID, and uses the
        current request user as the creator.
        """
        assignee = self._get_user_by_id(
            validated_data.pop('assignee_id', None))
        reviewer = self._get_user_by_id(
            validated_data.pop('reviewer_id', None))
        validated_data['created_by'] = self._get_request_user()

        return Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )

    def _get_user_by_id(self, user_id):
        """
        Retrieves a User instance by ID, or returns None if not found.
        """
        if not user_id:
            return None
        return User.objects.filter(id=user_id).first()

    def _get_request_user(self):
        """
        Returns the user from the serializer context's request.
        """
        return self.context['request'].user

    def __str__(self):
        """
        Returns a human-readable string representation of the Task.
        """
        return f"{self.title} ({self.status})"


class Comment(models.Model):
    """
    Represents a comment left by a user on a task.

    Includes the author, task, content, and timestamp.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Task'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    content = models.TextField(
        verbose_name='Content'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """
        Returns a human-readable string representation of the Comment.
        """
        return f"Comment by {self.author} on {self.created_at}"
