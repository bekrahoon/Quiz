from django import forms
from .models import Question
from django.contrib.auth.models import User  


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_option']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name']  