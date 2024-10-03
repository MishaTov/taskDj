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
            'first_name': forms.TextInput(attrs={'class': 'form-control wide', 'autocomplete': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control wide', 'autocomplete': True}),
            'username': forms.TextInput(attrs={'class': 'form-control wide', 'autocomplete': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password1_attrs = self.fields.get('password1').widget.attrs
        password2_attrs = self.fields.get('password2').widget.attrs
        password1_attrs['class'] = 'form-control wide'
        password2_attrs['class'] = 'form-control wide'
        password1_attrs['required'] = True
        password2_attrs['required'] = True
