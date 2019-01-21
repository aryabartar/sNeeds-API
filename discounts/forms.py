from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AddDiscountForm(forms.Form):
    discount_percent = forms.IntegerField(min_value=1, max_value=100,
                                          label="",
                                          widget=forms.TextInput(
                                              attrs={'placeholder': 'درصد تخفیف را وارد کنید (عدد بین 1 تا 100)',
                                                     'type': 'number',
                                                     'max': '100',
                                                     'min': '1'}))

    def clean_discount_percent(self):
        percent = self.cleaned_data['discount_percent']
        if int(percent) < 1:
            raise ValidationError(_('Invalid percent- Less than 1'))

        if int(percent) > 99:
            raise ValidationError(_('Invalid percent- More than 99'))

        return percent
