#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# Weka nambari hii juu ya block ya "if __name__ == '__main__':"
import os
from django.contrib.auth import get_user_model

def create_or_reset_admin():
    User = get_user_model()
    # Badilisha 'admin' kuwa username ya admin wako kama unaijua
    username = 'admin' 
    password = 'PasswordYakoMpya123!' # Weka password unayoitaka hapa
    email = 'admin@example.com'

    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.save()
        print(f"Password ya admin '{username}' imebadilishwa kikamilifu!")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Admin mpya '{username}' ametengenezwa kikamilifu!")

# Tafuta mstari huu uliokuwepo tayari kwenye manage.py, kisha weka amri yetu juu yake
if __name__ == '__main__':
    # Hapa ndipo tunapoita ile function yetu kabla ya server kuwaka
    import django
    django.setup()
    try:
        create_or_reset_admin()
    except Exception as e:
        print(e)
    main()

if __name__ == '__main__':
    main()
