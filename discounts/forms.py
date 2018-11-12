from django import forms
from django.core.exceptions import ValidationError


class AddDiscountForm(forms.Form):
    discount_percent = forms.IntegerField(min_value=1, max_value=100)

    def clean_discount_percent(self):
        percent = self.cleaned_data['discount_percent']
        if int(percent) < 1:
            raise ValidationError(_('Invalid percent- Less than 1'))

        if int(percent) > 99:
            raise ValidationError(_('Invalid percent- More than 99'))

        return percent
