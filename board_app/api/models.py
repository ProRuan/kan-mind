from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='boards')


class Task(models.Model):
    board = models.ForeignKey(
        Board, related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
                              ('to-do', 'To Do'), ('done', 'Done')])
    priority = models.CharField(max_length=20, choices=[(
        'low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
