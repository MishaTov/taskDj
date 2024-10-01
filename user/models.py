from os import urandom

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.db import models

from .validators import UsernamePatternValidator, NameValidator


def generate_default_username():
    return f'user_{urandom(12).hex()}'


def generate_default_password():
    return urandom(25).hex()


class CustomUser(AbstractUser):

    class Meta:
        db_table = 'users'

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True, default=generate_default_username, validators=[UsernamePatternValidator])
    password = models.CharField(max_length=128, default=generate_default_password, validators=[validate_password])
    first_name = models.CharField(max_length=50, blank=True, validators=[NameValidator])
    last_name = models.CharField(max_length=50, blank=True, validators=[NameValidator])
    first_login = models.BooleanField(default=True)
    assignment_limit = models.IntegerField(default=5)
    current_assignment_number = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} <{self.email}>'
