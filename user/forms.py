from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, BaseUserCreationForm


class AuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control wide'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control wide'})
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
            'first_name': forms.TextInput(attrs={'class': 'form-control wide'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control wide'}),
            'username': forms.TextInput(attrs={'class': 'form-control wide'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('password1').widget.attrs['class'] = 'form-control wide'
        self.fields.get('password1').widget.attrs['required'] = True
        self.fields.get('password2').widget.attrs['class'] = 'form-control wide'
        self.fields.get('password2').widget.attrs['required'] = True
