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

class UploadBooklet (forms.Form):
    title = forms.CharField(required=True,label="عنوان" )
    field = forms.CharField(required=True , label="رشته")
    topic = forms.CharField(required=True , label="درس")
    writer = forms.CharField(required=True,label="نویسنده")
    booklet_file = forms.FileField(required=True , label="آپلود جزوه")
    pass