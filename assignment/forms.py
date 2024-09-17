from datetime import timedelta

from django import forms
from django.utils.timezone import now


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


class AssignmentForm(forms.Form):
    date_widget = {'type': 'datetime-local',
                   'min': now().strftime('%Y-%m-%dT%H:%M'),
                   'max': (now() + timedelta(days=5 * 365)).strftime('%Y-%m-%dT%H:%M'),
                   'class': 'form-field'}
    worker_limit_choice = [(_, _) for _ in range(1, 11)]

    subject = forms.CharField(max_length=75, help_text='*', widget=forms.TextInput(attrs={'class': 'form-field'}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'class': 'form-field'}), required=False)
    deadline = forms.DateTimeField(widget=forms.DateInput(format='%d %b %Y %H:%M', attrs=date_widget), required=False)
    files = MultipleFileField(required=False)
    workers_limit = forms.ChoiceField(choices=worker_limit_choice, initial=5, widget=forms.Select(attrs={'class': 'form-field'}), required=False)
    priority = forms.ChoiceField(choices=((1, 'low'),
                                          (2, 'medium'),
                                          (3, 'high'),
                                          (4, 'critical')), widget=forms.Select(attrs={'class': 'form-field'}), required=False)
