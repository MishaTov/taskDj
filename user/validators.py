from re import fullmatch

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class FullMatchPatternValidator(RegexValidator):
    def __call__(self, value):
        regex_matches = self.regex.fullmatch(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            raise ValidationError(self.message, code=self.code, params={'value': value})


class PasswordPatternValidator(FullMatchPatternValidator):
    regex = r'[\w!@#$&*|]{8,50}'
    message = ('Your password must be from 8 to 50 characters '
               'and can contain latin letters, digits, underlines and ! @ # $ & * |')
    code = 'invalid_password'

    def validate(self, password, user=None):
        self.__call__(password)

    def get_help_text(self):
        return self.message


class UsernamePatternValidator(FullMatchPatternValidator):
    regex = r'^[a-zA-Z0-9]\w{3,28}[a-zA-Z0-9]$'
    message = ('Username must be from 5 to 30 characters and can contain latin letters, digits and underlines. '
               'Username cannot starts or ends with underline')
    code = 'invalid_username'


class NameValidator(FullMatchPatternValidator):
    regex = r'^(?!.*--)[A-Za-z]+(-[A-Za-z]+)*$'
    message = ('You can use only latin letters and hyphens. '
               'Field cannot starts or ends with hyphens as well as two or more hyphens cannot go in a row')
    code = 'invalid_name'
