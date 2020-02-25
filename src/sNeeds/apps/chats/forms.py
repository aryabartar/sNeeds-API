from django import forms

from .models import Message


class MessageFilterForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = "__all__"
