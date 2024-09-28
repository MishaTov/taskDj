from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'users'

    assignment_limit = models.IntegerField(default=5)
    current_assignment_number = models.IntegerField(default=0)

