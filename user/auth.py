from hashlib import sha256

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.urls import reverse_lazy

from user.models import CustomUser


class EmailUsernameAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        user = (user_model.objects.filter(email=username).first() or
                user_model.objects.filter(username=username).first())
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


def generate_registration_email(request, user: CustomUser):
    subject = 'Complete registration'
    message = ''
    login_link = request.build_absolute_uri(reverse_lazy('login_page'))
    html_message = (f'<div style="font-size: 20px">'
                    f'Your credentials for the <strong>FIRST</strong> login is: '
                    f'<p><strong>Email:</strong> {user.email}</p>'
                    f'<p><strong>Password:</strong> {user.password}</p>'
                    f'<p>You can use it to login <a href={login_link}>here<a>'
                    f'</div>')
    return subject, message, html_message


def hexdigest(data):
    return sha256(str(data).encode()).hexdigest()
