from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="آدرس ایمیل",
                             required=True,
                             max_length=120,
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'ایمیل خود را وارد نمایید'}
                             )
                             )

    phone_number_field = forms.CharField(required=True,
                                         label="شماره تماس",
                                         error_messages={'required': 'لطفا شماره تماس خود را وارد کنید'},
                                         max_length=12,
                                         widget=forms.TextInput(
                                             attrs={'placeholder': 'شماره موبایل خود را وارد نمایید'}
                                         ),
                                         )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2',
                  'phone_number_field',
                  )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
