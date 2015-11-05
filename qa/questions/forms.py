from django.forms import ModelForm
# from django import forms

from .models import Answer


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)
        # fields = ("text", "question")
        # widgets = {"question": forms.HiddenInput()}
