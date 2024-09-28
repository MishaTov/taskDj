from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class Login(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm
