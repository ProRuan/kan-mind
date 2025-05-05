from django.db import models

# Create your models here.

# review!
STATUS_CHOICES = [
    ('to-do', 'To Do'),
    ('in-progress', 'In Progress'),
    ('done', 'Done'),
]

# review!
PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


# {
#     "id": 1,
#     "board": 1,
#     "title": "Task 1",
#     "description": "Beschreibung der Task 1",
#     "status": "to-do",
#     "priority": "high",
#     "assignee": {
#       "id": 13,
#       "email": "marie.musterfraun@example.com",
#       "fullname": "Marie Musterfrau"
#     },
#     "reviewer": {
#       "id": 1,
#       "email": "max.mustermann@example.com",
#       "fullname": "Max Mustermann"
#     },
#     "due_date": "2025-02-25",
#     "comments_count": 0
#   },


class Contact(models.Model):
    email = models.EmailField(max_length=255, unique=True, default='')
    fullname = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.fullname


class Task(models.Model):
    board = models.IntegerField()  # Replace with ForeignKey if you have a Board model
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=400, blank=True, default='')
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(
        max_length=32, choices=PRIORITY_CHOICES, default='medium')
    assignee = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, related_name='reviewed_tasks')
    due_date = models.DateField()
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# for POST
# --------
# {
#   "board": 12,
#   "title": "Code-Review durchführen",
#   "description": "Den neuen PR für das Feature X überprüfen",
#   "status": "review",
#   "priority": "medium",
#   "assignee_id": 13,
#   "reviewer_id": 1,
#   "due_date": "2025-02-27"
# }
