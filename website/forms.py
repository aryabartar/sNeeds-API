from django import forms
from .models import Booklet


class UploadBookletForm(forms.ModelForm):
    class Meta:
        model = Booklet
        fields = ['title',
                  'owner',
                  'topic',
                  'booklet_content',
                  'booklet_image',
                  ]


class UploadBooklet(forms.Form):
    title = forms.CharField(required=True, label="عنوان*", error_messages={'required': 'لطفا فیلد را پر کنید'})
    field = forms.CharField(required=True, label="رشته*", error_messages={'required': 'لطفا فیلد را پر کنید'})
    topic = forms.CharField(required=True, label="درس*", error_messages={'required': 'لطفا فیلد را پر کنید'})
    writer = forms.CharField(required=False, label="نویسنده", error_messages={'required': 'لطفا فیلد را پر کنید'})
    booklet_file = forms.FileField(required=True, label="آپلود جزوه*",
                                   error_messages={'required': 'لطفا فیلد را پر کنید'})


class SearchBooklet(forms.Form):
    search_bar = forms.CharField(required=True, error_messages={'required': 'لطفا عنوان را مشخص کنید'})


class SearchBar (forms.Form) :
    search_bar = forms.CharField(required=True , label="جستجو" , error_messages={'required': 'لطفا فرم را پر کنید'}, max_length=120)