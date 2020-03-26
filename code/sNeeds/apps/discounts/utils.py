import datetime
import os
import random
import string


def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_discount_code_generator(instance):
    """
    This is for a Django project with an tracing_code field
    """
    discount_new_code = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(code=discount_new_code).exists()
    if qs_exists:
        return unique_discount_code_generator(instance)
    return discount_new_code
