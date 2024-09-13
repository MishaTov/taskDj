from datetime import timedelta

from django import forms
from django.utils.timezone import now


class AssignmentForm(forms.Form):
    date_widget = {'type': 'datetime-local',
                   'min': now().strftime('%Y-%m-%dT%H:%M'),
                   'max': (now() + timedelta(days=5 * 365)).strftime('%Y-%m-%dT%H:%M')}

    subject = forms.CharField(max_length=75, help_text='*')
    description = forms.CharField(max_length=5000, widget=forms.Textarea, required=False)
    deadline = forms.DateTimeField(widget=forms.DateInput(format='%d %b %Y %H:%M', attrs=date_widget), required=False)
    files = forms.FileField(required=False)
    workers_limit = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                               (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)), required=False)
    priority = forms.ChoiceField(choices=((1, 'low'),
                                          (2, 'medium'),
                                          (3, 'high'),
                                          (4, 'critical')), required=False)
