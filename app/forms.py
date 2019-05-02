"""
app.forms
"""
from django import forms

from .models import Programming


class ProgrammingForm(forms.ModelForm):
    """ProgrammingForm"""
    class Meta:
        model = Programming
        exclude = []


class FileUplaodForm(forms.Form):
    file = forms.ImageField()
