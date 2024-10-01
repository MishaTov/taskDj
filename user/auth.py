from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib import messages


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user and user.check_password(password):
                if user.first_login:
                    messages.info(request, 'Check your email for further instructions to complete registration')
                return user
            return None
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
