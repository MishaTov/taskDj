from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from user.models import CustomUser


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model: CustomUser = get_user_model()
        user = (user_model.objects.filter(email=username).first() or
                user_model.objects.filter(username=username).first())
        if not user:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
