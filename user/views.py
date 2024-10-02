from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class Login(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm
    form_class.error_messages['invalid_login'] = 'Incorrect username/email or password'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.first_login:
            return redirect('registration', username=user.username)
        else:
            return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('assignment_list')


class CreateProfile(View):
    def get(self):
        pass

    def post(self):
        pass


def registration(request, username):
    if request.user.username == username:
        return render(request, 'user/registration_page.html')
    return HttpResponseNotFound('page not found')
