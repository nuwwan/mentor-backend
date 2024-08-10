from django.db import models

class Subject(models.TextChoices):
    FINANCE='fin','Finance'
    EDUCATION='edu','Education'