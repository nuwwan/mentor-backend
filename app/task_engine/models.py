from django.db import models
from user.models import AuthUser
from .enums import Subject, PrivacyChoices


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Timeline(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="timelines"
    )
    subject = models.CharField(max_length=3, choices=Subject.choices)
    created_on = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=10, choices=PrivacyChoices.choices)

    def __str__(self) -> str:
        return self.title


class Mentorship(models.Model):
    mentor = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="mentees"
    )
    mentee = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="mentors"
    )
    timeline = models.ForeignKey(
        Timeline, on_delete=models.CASCADE, related_name="mentorships"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=3, choices=Subject.choices)

    def __str__(self) -> str:
        return f"mentor:{self.mentor.id} mentee:{self.mentee.id}"


class Peer(models.Model):
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="peer_from"
    )
    peer = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="peer_to")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"from:{self.user.id} to:{self.peer.id}"

    def save(self, *args, **kwargs):
        # ensure the bidirectional relationship
        if not Peer.objects.filter(user=self.peer, peer=self.user).exists():
            Peer(user=self.peer, peer=self.peer).save()
        super().save(*args, **kwargs)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self) -> str:
        return self.title


class Milestone(models.Model):
    title = models.CharField(max_length=200)
    timeline = models.ForeignKey(
        Timeline, on_delete=models.CASCADE, related_name="milestones"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="milestones"
    )

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="tasks"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through="TaskTag", related_name="tasks")

    def __str__(self) -> str:
        return self.title


class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class TimelineTask(models.Model):
    timeline = models.ForeignKey(
        Timeline, on_delete=models.CASCADE, related_name="tasks"
    )
    owner = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="timeline_tasks"
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="timeline_tasks"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"timeline id:{self.timeline.id}  task id:{self.task.id}"
