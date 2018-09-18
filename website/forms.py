from django import forms
from .models import Booklet


class UploadBookletForm(forms.ModelForm):
    class Meta:
        model = Booklet
        fields = ['title',
                  'owner',
                  'topic',
                  'text',
                  'booklet_content',
                  'booklet_image',
                  ]
