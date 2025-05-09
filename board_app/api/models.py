"""
Models for the board application.
Defines the structure and constraints for the Board entity.
"""

# Third-party suppliers
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Board(models.Model):
    """
    A Board represents a collaborative space owned by a user
    and shared with other user members for managing tasks.
    """

    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(
            3, message="Title must be at least 3 characters long.")],
        help_text="Title of the board (required, minimum 3 characters)."
    )
    owner = models.ForeignKey(
        User,
        related_name='owned_boards',
        on_delete=models.CASCADE,
        help_text="User who created and owns the board."
    )
    members = models.ManyToManyField(
        User,
        related_name='boards',
        blank=True,
        help_text="Users who are members of this board."
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ['title']
