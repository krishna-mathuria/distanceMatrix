from django import forms
from .models import History


class FileForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('origin', 'destination')