from django.db import models


class Subject(models.TextChoices):
    FINANCE = "fin", "Finance"
    EDUCATION = "edu", "Education"


class PrivacyChoices(models.TextChoices):
    OWNER_ONLY = "own", "Owner Only"
    MENTOR_OWNER = "mnt_own", "Mentor Owner"
    PUBLIC = "pub", "Public"
