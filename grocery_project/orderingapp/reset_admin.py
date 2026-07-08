import os
import django

# Weka mazingira ya Django (Settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_project.settings') # Kama jina la folda la settings ni tofauti, badilisha hapa
django.setup()

from django.contrib.auth import get_user_model

def reset():
    User = get_user_model()
    username = 'jolinyo'
    password = 'jolinyo001' # Hii ndio itakuwa password yako mpya
    email = 'jolinyoalex@gmail.com'

    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.save()
        print(f"✅ SUCCESS: Password ya admin '{username}' imebadilishwa kikamilifu kule Render!")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ SUCCESS: Admin mpya '{username}' ametengenezwa kikamilifu kule Render!")

if __name__ == '__main__':
    reset()