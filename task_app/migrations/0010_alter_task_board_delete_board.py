# Generated by Django 5.1.4 on 2025-05-07 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0003_alter_board_owner'),
        ('task_app', '0009_alter_task_assignee_alter_task_reviewer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='board_app.board'),
        ),
        migrations.DeleteModel(
            name='Board',
        ),
    ]
