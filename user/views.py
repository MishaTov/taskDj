from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .auth import hexdigest
from .forms import AuthForm, CompleteRegistrationForm


class Login(LoginView):
    template_name = 'user/login.html'
    form_class = AuthForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.first_login:
            email_hash = hexdigest(user.email)
            return redirect('registration', email_hash=email_hash)
        else:
            return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('assignment_list')


class CompleteRegistration(UpdateView):
    template_name = 'user/registration_page.html'
    form_class = CompleteRegistrationForm
    model = get_user_model()
    success_url = reverse_lazy('assignment_list')

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if hexdigest(user.email) == kwargs.get('email_hash'):
            setattr(self, 'object', user)
            return self.render_to_response(self.get_context_data())
        return HttpResponseNotFound('page not found')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_login = False
        user.save()
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        email = getattr(self.request.user, 'email', False)
        user = get_object_or_404(self.model, email=email)
        return user
