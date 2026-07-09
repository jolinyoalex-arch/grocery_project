import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery.settings') # Hakikisha jina la mradi wako lipo sahihi hapa
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin_mpya'
email = 'admin@gmail.com'
password = 'PasswordYako123!'

if not User.objects.filter(username=username).exists():
    print(f"Inatengeneza admin: {username}")
    User.objects.create_superuser(username, email, password)
    print("Admin ametengenezwa kikamilifu!")
else:
    print("Admin tayari yupo, inabadilisha password...")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print("Password imebadilishwa!")