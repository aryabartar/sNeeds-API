import datetime
import os
import random
import string


def random_string_generator(size=12, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_consultant_deposit_info_id_generator(instance):
    """
    This is for a Django project with an consultant_deposit_info_id field
    """
    new_consultant_deposit_info_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(consultant_deposit_info_id=new_consultant_deposit_info_id).exists()
    if qs_exists:
        return unique_consultant_deposit_info_id_generator(instance)
    return new_consultant_deposit_info_id
