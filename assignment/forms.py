from django import forms


class AssignmentForm(forms.Form):

    subject = forms.CharField(max_length=50, help_text='*')
    description = forms.CharField(max_length=5000, widget=forms.Textarea, required=False)
    deadline = forms.DateTimeField(widget=forms.SelectDateWidget, required=False)
    files = forms.FileField(required=False)
    workers_limit = forms.IntegerField(max_value=10, min_value=1, initial=5)
    priority = forms.ChoiceField(required=False)
