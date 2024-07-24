from django.db import models
from authentication.models import AuthUser


class Profile(models.Model):
    base_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    is_mentee = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    title = models.CharField(max_length=5)
    gender = models.CharField(max_length=10)
    birth_year = models.IntegerField()
    birth_month = models.IntegerField()
    birth_date = models.IntegerField()
    country_origin = models.CharField(max_length=30)
    country_live = models.CharField(max_length=30, null=True)
    age = models.IntegerField()
    profile_photo = models.CharField(max_length=200, null=True)
