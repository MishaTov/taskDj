from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class Login(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.first_login:
            return redirect('registration', username=user.username)
        else:
            return redirect(self.get_success_url())

    def form_invalid(self, form):
        user_model = get_user_model()
        username = form.cleaned_data.get('username')
        try:
            user = (user_model.objects.filter(email=username).first() or
                    user_model.objects.filter(username=username).first())
            if user.first_login:
                messages.info(self.request, 'Check your email for further instructions to complete registration')
            else:
                password_field = form.fields.get('password')
                password_widget_class = str(password_field.widget.attrs.get('class'))
                password_field.widget.attrs['class'] = password_widget_class + ' invalid'
                form.add_error('password', 'Wrong password')
        except user_model.DoesNotExist:
            username_field = form.fields.get('username')
            username_widget_class = str(username_field.widget.attrs.get('class'))
            username_field.widget.attrs['class'] = username_widget_class + ' invalid'
            form.add_error('username', 'User not found')
        return self.render_to_response(self.get_context_data(form=form))

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
