from .models import Submission
from django import forms
class UserStatus(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('status')