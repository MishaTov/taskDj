from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from .forms import AuthForm, CompleteRegistrationForm


class Login(LoginView):
    template_name = 'user/login.html'
    form_class = AuthForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.first_login:
            return redirect('registration', username=user.username)
        else:
            return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('assignment_list')


class CompleteRegistration(UpdateView):
    template_name = 'user/registration_page.html'
    form_class = CompleteRegistrationForm
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        if self.request.user.username != kwargs.get('username'):
            return HttpResponseNotFound('page not found')
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = ''
        return initial
