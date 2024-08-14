from django.db import models


class Subject(models.TextChoices):
    FINANCE = "fin", "Finance"
    EDUCATION = "edu", "Education"


class PrivacyChoices(models.TextChoices):
    OWNER_ONLY = "owner", "Owner Only"
    MENTOR_OWNER = "mentor_owner", "Mentor Owner"
    PUBLIC = "public", "Public"
