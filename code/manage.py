#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    DEPLOYMENT = int(os.environ.get('DJANGO_DEPLOYMENT', default=0))

    if DEPLOYMENT == 0:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sNeeds.settings.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sNeeds.settings.deployment')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
