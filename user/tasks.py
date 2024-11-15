from celery import shared_task
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail

from .models import CustomUser


@shared_task
def send_password_reset_email(*args, **kwargs):
    context = args[2]
    context['user'] = CustomUser.objects.get(pk=context['user'])
    PasswordResetForm.send_mail(None, *args, **kwargs)


@shared_task
def send_registration_email(*args, **kwargs):
    send_mail(*args, **kwargs)
