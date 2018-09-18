from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="آدرس ایمیل", required=True, widget=forms.EmailInput(), max_length=120)
    phone_number_field = forms.CharField(required=True, label="شماره تماس",
                                         error_messages={'required': 'لطفا شماره تماس خود را وارد کنید'}, max_length=12)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'phone_number_field',
                  'password1',
                  'password2'
                  )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
