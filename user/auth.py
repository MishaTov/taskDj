from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.shortcuts import redirect


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user and user.check_password(password):
                if user.first_login:
                    redirect('create_profile', user=user)
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
