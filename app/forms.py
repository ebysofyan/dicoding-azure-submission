"""
app.forms
"""
from django.forms import ModelForm

from .models import Programming


class ProgrammingForm(ModelForm):
    """ProgrammingForm"""
    class Meta:
        model = Programming
        exclude = []
