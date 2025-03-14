from datetime import timedelta, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from .models import Assignment, File, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'description', 'deadline', 'workers_limit', 'priority']
        date_widget = {'type': 'datetime-local',
                       'min': (now() + timedelta()).strftime('%Y-%m-%dT%H:%M'),
                       'max': (now() + timedelta(days=5 * 365)).strftime('%Y-%m-%dT%H:%M')}
        widgets = {
            'deadline': forms.DateInput(format='%d %b %Y %H:%M', attrs=date_widget),
        }
        help_texts = {
            'subject': '*'
        }
        error_messages = {
            'subject': {
                'required': 'This field must be filled',
                'max_length': 'This field cannot be longer than 75 characters'
            },
            'description': {
                'max_length': 'This field cannot be longer than 5000 characters'
            },
            'workers_limit': {
                'invalid_choice': 'You must provide a value from 1 to 10 inclusive'
            },
            'priority': {
                'invalid_choice': 'You must provide one of the next variants: Low, Medium, High, Critical'
            }
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline:
            if deadline <= now():
                raise ValidationError('You cannot set a deadline in the past')
            if deadline >= now() + timedelta(days=5*365):
                raise ValidationError('You cannot set a deadline further than 5 years from now')
            return deadline


class FileForm(forms.Form):
    file = MultipleFileField(required=False)

    def clean_file(self, size_limit=15):
        for file in self.files.getlist('file'):
            if file.size > size_limit * 1024 * 1024:
                raise ValidationError(f'Max allowed file size is {size_limit}Mb')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your comment here'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if not user.is_authenticated:
            self.fields['content'].widget.attrs.update({
                'placeholder': 'You must be logged in to post comments',
                'disabled': True
            })


class FilterForm(forms.Form):
    date_widget = {'type': 'datetime-local',
                   'min': datetime(year=2024, month=1, day=1).strftime('%Y-%m-%dT%H:%M'),
                   'max': (now() + timedelta(days=7 * 365)).strftime('%Y-%m-%dT%H:%M')}
    status_choices = [
        (Assignment.Status.PENDING, Assignment.Status.PENDING),
        (Assignment.Status.PROGRESS, Assignment.Status.PROGRESS),
        (Assignment.Status.DONE, Assignment.Status.DONE),
        (Assignment.Status.FAILED, Assignment.Status.FAILED)
    ]
    priority_choices = Assignment.PRIORITY_CHOICES

    created_by = forms.CharField(max_length=30, required=False)
    deadline_from = forms.DateTimeField(widget=forms.DateInput(format='%d %b %Y %H:%M', attrs=date_widget), required=False)
    deadline_to = forms.DateTimeField(widget=forms.DateInput(format='%d %b %Y %H:%M', attrs=date_widget), required=False)
    status = forms.MultipleChoiceField(choices=status_choices, widget=forms.CheckboxSelectMultiple, required=False)
    priority = forms.MultipleChoiceField(choices=priority_choices, widget=forms.CheckboxSelectMultiple, required=False)
