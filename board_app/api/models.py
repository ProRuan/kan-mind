from django.db import models
# from django.contrib.auth.models import User


from task_app.api.models import Task


class Board(models.Model):
    title = models.CharField(max_length=255)
    tasks = Task.objects.all()
    # owner = models.ForeignKey(User, related_name="owned_boards", on_delete=models.CASCADE)
    # members = models.ManyToManyField(User, related_name="boards", blank=True)

    # def member_count(self):
    #     return self.members.count()

    def ticket_count(self):
        return self.tasks.count()

    def tasks_to_do_count(self):
        return self.tasks.filter(status='to_do').count()

    def tasks_high_prio_count(self):
        return self.tasks.filter(priority='high').count()

    def __str__(self):
        return self.title
