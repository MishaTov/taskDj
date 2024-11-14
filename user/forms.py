from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, BaseUserCreationForm
from django.contrib.auth.forms import PasswordResetForm as PwdResForm

from .tasks import send_reset_email


class AuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
    error_messages = {
        'invalid_login': 'Incorrect username/email or password',
        'inactive': 'This account is inactive',
    }


class CompleteRegistrationForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'autocomplete': True}),
            'last_name': forms.TextInput(attrs={'autocomplete': True}),
            'username': forms.TextInput(attrs={'autocomplete': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password1_attrs = self.fields.get('password1').widget.attrs
        password2_attrs = self.fields.get('password2').widget.attrs
        password1_attrs['required'] = True
        password2_attrs['required'] = True
