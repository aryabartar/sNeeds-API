import datetime
import os
import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_tracing_code_generator(instance):
    """
    This is for a Django project with an tracing_code field
    """
    new_consultant_deposit_tracing_code = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(tracing_code=new_consultant_deposit_tracing_code).exists()
    if qs_exists:
        return unique_tracing_code_generator(instance)
    return new_consultant_deposit_tracing_code
