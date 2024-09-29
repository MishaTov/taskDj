from django.db import models
from django.contrib.auth.models import AbstractUser
from os import urandom
from re import fullmatch


def validate_username(username):
    return fullmatch(r'^[a-zA-Z0-9]\w{3,28}[a-zA-Z0-9]$', username)


def validate_password(password):
    return fullmatch(r'[\w!@#$%&*]{8,50}', password)


class User(AbstractUser):

    class Meta:
        db_table = 'users'

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(unique=True, default=f'user_{urandom(12).hex()}', validators=[validate_username])
    first_login = models.BooleanField(default=True)
    assignment_limit = models.IntegerField(default=5)
    current_assignment_number = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username} <{self.email}>'
