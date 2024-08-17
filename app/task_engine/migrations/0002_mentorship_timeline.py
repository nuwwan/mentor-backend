# Generated by Django 5.1 on 2024-08-14 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_engine", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mentorship",
            name="timeline",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mentorships",
                to="task_engine.timeline",
            ),
            preserve_default=False,
        ),
    ]
