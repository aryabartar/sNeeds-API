from django.contrib.auth.password_validation import MinimumLengthValidator


class MinimumLengthValidator(MinimumLengthValidator):
    def __init__(self):
        super().__init__(min_length=6)
