from django import forms


class AddDiscountForm(forms.Form):
    discount_percent = forms.IntegerField(min_value=1, max_value=100)
