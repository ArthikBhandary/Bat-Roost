from django import forms

from .models import Submission


class UserStatus(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('status')