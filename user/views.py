from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views import View

class Login(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm


class CreateProfile(View):
    def get(self):
        pass

    def post(self):
        pass
