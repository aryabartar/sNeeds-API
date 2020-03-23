import datetime
import os
import random
import string
from .models import Discount


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_discount_code_generator():
    """
    This is for a Django project with an tracing_code field
    """
    new_discount_code = random_string_generator()

    qs_exists = Discount.objects.filter(code=new_discount_code).exists()
    if qs_exists:
        return unique_discount_code_generator()
    return new_discount_code
