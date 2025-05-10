# Third-party suppliers
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Board(models.Model):
    """
    A Board represents a collaborative workspace.

    Each board is owned by a user (the creator) and can be shared with other users
    (members). Boards can be used to manage and organize tasks collaboratively.
    """

    title = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(
                3,
                message="Title must be at least 3 characters long."
            )
        ],
        help_text="Title of the board (required, minimum 3 characters)."
    )

    owner = models.ForeignKey(
        User,
        related_name='owned_boards',
        on_delete=models.CASCADE,
        help_text="The user who owns the board."
    )

    members = models.ManyToManyField(
        User,
        related_name='boards',
        blank=True,
        help_text="Other users who have access to this board."
    )

    def __str__(self):
        """
        Return a string representation of the board.

        Returns:
            str: The title of the board.
        """
        return self.title

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ['title']
